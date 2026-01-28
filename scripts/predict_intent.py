import joblib
import pandas as pd
import numpy as np

# 1. Load the trained model
MODEL_PATH = '/Users/srujan/Desktop/customer-purchase-intelligence/models/purchase_predictor.pkl'
model = joblib.load(MODEL_PATH)

def predict_purchase_intent(total_interactions, view_count, unique_products, avg_price, session_duration, view_to_cart_ratio, start_hour, is_weekend):
    """
    Takes customer session data and returns a purchase prediction.
    """
    # Create a DataFrame matching the model's training features
    data = {
        'total_interactions': [total_interactions],
        'view_count': [view_count],
        'unique_products_viewed': [unique_products],
        'avg_price_interacted': [avg_price],
        'session_duration_sec': [session_duration],
        'view_to_cart_ratio': [view_to_cart_ratio],
        'start_hour': [start_hour],
        'is_weekend': [is_weekend]
    }
    
    df = pd.DataFrame(data)
    
    # Get prediction and probability
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1] # Probability of being a '1'
    
    return prediction, probability

# --- TEST THE SCRIPT ---
if __name__ == "__main__":
    print("🔮 Running Intent Prediction Test...")
    
    # Simulation: A highly engaged user
    pred, prob = predict_purchase_intent(
        total_interactions=15, 
        view_count=10, 
        unique_products=5, 
        avg_price=150.0, 
        session_duration=600, 
        view_to_cart_ratio=0.5, 
        start_hour=14, 
        is_weekend=0
    )
    
    status = "PURCHASE LIKELY" if pred == 1 else "NO PURCHASE LIKELY"
    print(f"Result: {status} (Confidence: {prob:.2%})")