import streamlit as st
import numpy as np
import pandas as pd
import pickle
import gdown  # To download the model file from Google Drive 

# Function to load the model from a local file
def load_model():
    model_path = "sales_prediction_model.pkl"
    
    # Download the model from Google Drive 
    try:
        with open(model_path, 'rb') as file:
            loaded_model = pickle.load(file)
    except FileNotFoundError:
        st.warning("Model not found locally. Downloading from Google Drive...")
        # Replace this with your actual file ID
        file_id = "1kn587zK38ksriYbVekq67Mud4w5hMLFs"
        download_url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(download_url, model_path, quiet=False)
        with open(model_path, 'rb') as file:
            loaded_model = pickle.load(file)
    return loaded_model

# Function to make predictions
def sales_prediction(input_data):
    # Define column names as expected by the model
    column_names = [
        "Item_Weight", "Item_Fat_Content", "Item_Visibility", 
        "Item_Type", "Item_MRP", "Outlet_Establishment_Year", 
        "Outlet_Size", "Outlet_Location_Type", "Outlet_Type"
    ]
    
    # Create a DataFrame for the input data
    input_data_as_dataframe = pd.DataFrame([input_data], columns=column_names)
    
    # Make a prediction using the loaded model
    prediction = loaded_model.predict(input_data_as_dataframe)
    return prediction[0]

# Load the model once at the start
loaded_model = load_model()

# Streamlit App
def main():
    st.title("Sales Prediction Web Application (Streamlit)")
    st.write("Enter the store and item details below to predict sales.")

    # User inputs
    Item_Weight = st.number_input("Item Weight (in kg)", min_value=0.0, step=0.1)
    Item_Fat_Content = st.selectbox("Item Fat Content", ["-Select-", "Low Fat", "Regular", "Non-Edible"])
    Item_Visibility = st.number_input("Item Visibility", min_value=0.0, max_value=1.0, step=0.01)
    Item_Type = st.selectbox("Item Type", [
        "-Select-","Baking Goods", "Breads", "Breakfast", "Canned", "Dairy", 
        "Frozen Foods", "Fruits and Vegetables", "Hard Drinks", 
        "Health and Hygiene", "Household", "Meat", "Others", 
        "Seafood", "Snack Foods", "Soft Drinks", "Starchy Foods"
    ])
    Item_MRP = st.number_input("Item MRP (in currency)", min_value=0.0, step=1.0)
    Outlet_Establishment_Year = st.number_input("Outlet Establishment Year", min_value=1950, max_value=2024, step=1)
    Outlet_Size = st.selectbox("Outlet Size", ["-Select-", "Small", "Medium", "High"])
    Outlet_Location_Type = st.selectbox("Outlet Location Type", ["-Select-", "Tier 1", "Tier 2", "Tier 3"])
    Outlet_Type = st.selectbox("Outlet Type", ["-Select-", "Grocery Store", "Supermarket Type1", "Supermarket Type2", "Supermarket Type3"])

    # Prediction
    if st.button("Predict Sales"):
        input_data = [
            Item_Weight, Item_Fat_Content, Item_Visibility, 
            Item_Type, Item_MRP, Outlet_Establishment_Year, 
            Outlet_Size, Outlet_Location_Type, Outlet_Type
        ]
        try:
            prediction = sales_prediction(input_data)
            st.success(f"Predicted Sales: {prediction:.2f}")
        except Exception as e:
            st.error(f"Error in prediction: {e}")

if __name__ == '__main__':
    main()
