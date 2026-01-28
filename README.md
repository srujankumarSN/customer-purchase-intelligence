# 🛒 E-Commerce Purchase Intent Prediction

How I predicted customer purchases with 97% precision using a 5GB dataset.

---

🎯 The Objective:

Built an end-to-end data pipeline to predict customer purchase intent using high-volume behavioral logs. By analyzing how users browse, the system identifies potential buyers with a 0.91 F1-Score, allowing businesses to target high-intent customers in real-time.

---

🛠️ Tech Stack

Data Engineering: Python (Pandas Chunks), PostgreSQL 18, SQLAlchemy.

Machine Learning: Scikit-learn (Random Forest), NumPy.

Environment: macOS (M3 Native), Git LFS.

---

🏗️ The Pipeline (Phase-by-Phase):

Phase A: Data Engineering (The Foundation)

    Scalable Ingestion: Developed a Python-based ETL pipeline using pandas chunks to migrate 5GB+ of raw CSV data into PostgreSQL without exceeding local memory limits.

    Medallion Architecture: Structured a "Bronze" layer (events_raw) and a "Silver" layer (customer_features) to maintain data lineage and clean analytical features.

Phase B: Exploratory Data Analysis (The Insights)

    Behavioral Trends: Discovered a 6.81% conversion rate. Analysis showed browsing peaks at 3:00 PM, but purchasing is tied to specific engagement signals rather than time of day.

    Feature Validation: Used Pearson correlation heatmaps to prove that view_to_cart_ratio was the primary driver of revenue.

Phase C: Machine Learning (The Intelligence)

    This phase focused on solving two critical real-world challenges:

    Handling Class Imbalance: With only 6.81% buyers, I implemented Stratified Splitting and Balanced Class Weights. This prevented the model from simply guessing "No Purchase" and forced it to learn the characteristics of actual buyers.

    Resolving Data Leakage: Initial runs showed 100% accuracy. I identified "future information" (leakage) in the features and performed Feature Pruning. This dropped accuracy to a realistic 99%, ensuring the model predicts intent based on browsing, not just looking at the final receipt.

Phase D: Production Readiness

    Serialization: Exported the trained weights into a .pkl file using Git LFS for portable deployment.

    Inference Utility: Created predict_intent.py, a standalone script for generating real-time purchase probabilities.

📊 Key Results

    97% Precision: Extremely low false-positive rate; when the model predicts a purchase, it is almost always right.

    0.91 F1-Score: Successfully balanced the 93/7 class imbalance to provide a reliable business tool.

    Top Predictors: Identified Total Interactions and Session Duration as the most significant non-leaky indicators of intent.

📂 Project Structure

├── data       # Source CSVs (Local only / .gitignore)

├── sql        # Database Schema & Transformations

├── scripts    # ETL & Ingestion Logic (ingest_data.py)

├── notebooks  # EDA & Model Training (Phase B & C)

├── models     # Saved ML Models (.pkl via Git LFS)

├── config     # Environment variables (.env)

└── docs       # Final Report & Visualizations

---

🚀 Getting Started

    Clone the repo: git clone https://github.com/your-username/customer-purchase-intelligence.git

    Install dependencies: pip install -r requirements.txt

    Setup Kaggle API: Ensure your kaggle.json is in ~/.kaggle/.

    Run Ingestion: python scripts/ingest_data.py