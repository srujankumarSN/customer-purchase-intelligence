import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Set these BEFORE importing kaggle
os.environ['KAGGLE_USERNAME'] = "srujankumar"
os.environ['KAGGLE_KEY'] = "KGAT_53b767ebc4300d81616828247f71704a" # Note: Use KAGGLE_KEY, not KAGGLE_API_TOKEN


# 1. Load Environment Variables (.env)
load_dotenv()

# --- CONFIGURATION ---
DB_NAME = "ecommerce_db"
DB_USER = "postgres"
DB_PASS = os.getenv("DB_PASS") # Loads from your .env file
DB_HOST = "localhost"
DB_PORT = "5432"

DATA_DIR = "./data"
FILE_NAME = "2019-Oct.csv"
FILE_PATH = os.path.join(DATA_DIR, FILE_NAME)
#import kagglehub

# Download latest version
# path = kagglehub.dataset_download("mkechinov/ecommerce-behavior-data-from-multi-category-store")

# print("Path to dataset files:", path)
KAGGLE_DATASET = "mkechinov/ecommerce-behavior-data-from-multi-category-store"

def ensure_data_exists():
    """Checks for local data; downloads from Kaggle if missing."""
    if not os.path.exists(FILE_PATH):
        print(f"📂 {FILE_NAME} not found. Initializing Kaggle download...")
        os.makedirs(DATA_DIR, exist_ok=True)
        
        try:
            import kaggle
            kaggle.api.authenticate()
            # This downloads and unzips the specific dataset
            kaggle.api.dataset_download_files(KAGGLE_DATASET, path=DATA_DIR, unzip=True)
            print("✅ Download and extraction complete.")
        except Exception as e:
            print(f"❌ Kaggle API Error: {e}. Ensure kaggle.json is in ~/.kaggle/")
            return False
    else:
        print(f"✅ {FILE_NAME} found. Skipping download.")
    return True

def ingest_to_postgres():
    """Streams data into PostgreSQL in memory-efficient chunks."""
    # Create the connection string
    db_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(db_url)
    
    print(f"🚀 Starting ingestion into '{DB_NAME}'...")
    
    try:
        # We use a chunksize of 100k to stay within M3 memory limits
        chunk_iter = pd.read_csv(FILE_PATH, chunksize=100000)
        
        for i, chunk in enumerate(chunk_iter):
            # Clean column names to match SQL schema
            chunk.columns = [c.strip() for c in chunk.columns]
            
            # Use 'append' because the table was created by your SQL script
            chunk.to_sql('events_raw', engine, if_exists='append', index=False)
            
            if (i + 1) % 5 == 0:
                print(f"📦 Progress: { (i+1) * 100000 } rows loaded...")
                
        print("🔥 All data successfully loaded into PostgreSQL!")
        
    except Exception as e:
        print(f"❌ Ingestion Error: {e}")

if __name__ == "__main__":
    if ensure_data_exists():
        ingest_to_postgres()