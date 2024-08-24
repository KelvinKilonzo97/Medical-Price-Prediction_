import pickle
import streamlit as st
import numpy as np
import base64

# Load the trained model
model = pickle.load(open("C:/Users/Kelvin/OneDrive/Documents/iiAfrica/Medical Price Prediction/random_forest_model.pkl", 'rb'))

# Create dictionaries for categorical variable encoding
sex_dict = {'female': 0, 'male': 1}
smoker_dict = {'no': 0, 'yes': 1}
region_dict = {'northeast': 0, 'northwest': 1, 'southeast': 2, 'southwest': 3}
# Path to your background image
#bg_image_path = "HospitalView.png"  # Make sure this image is in the correct location relative to the app script

# Convert the image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image_path = "HospitalView.png"
bg_image_base64 = get_base64_of_bin_file(bg_image_path)

def main():
    st.title("Medical Price Prediction")

    # Inject CSS to set the background image
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_image_base64}");
            background-size: cover;
            background-position: center;
            position: relative;
        }}
        .stApp::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);  /* Semi-transparent overlay */
            z-index: 0;
        }}
        .stApp > div {{
            position: relative;
            z-index: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Input variables
    age = st.text_input("Age")
    bmi = st.text_input("BMI")
    sex = st.selectbox("Gender", ['female', 'male'])
    children = st.text_input("Number of children")
    smoker = st.selectbox("Are you a smoker?", ['no', 'yes'])
    region = st.selectbox("Which region do you come from?", ['northeast', 'northwest', 'southeast', 'southwest'])

    # Encode categorical variables using dictionaries
    sex_encoded = sex_dict[sex]
    smoker_encoded = smoker_dict[smoker]
    region_encoded = region_dict[region]

    # Prediction
    if st.button("Predict"):
        # Convert inputs to a NumPy array before passing to the model
        input_data = np.array([[age, bmi, sex_encoded, children, smoker_encoded, region_encoded]])
        makeprediction = model.predict(input_data)
        output = round(makeprediction[0], 2)
        st.success(f'Your predicted medical cost: ${output}')

if __name__ == '__main__':
    main()
