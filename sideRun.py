import streamlit as st
import tensorflow as tf
from keras_preprocessing.image import img_to_array
from keras.models import load_model
from PIL import Image
import numpy as np
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import webbrowser
import matplotlib.pyplot as plt
st.set_page_config(page_title="My App", page_icon=":rocket:", layout="centered")

# --- USER AUTHENTICATION ---
names=["Pratham Kotian","Pujari Sanmith","Gautham Ghetia","Jash"]
usernames=["pratham","sanmith","gautham","jash"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=7)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
# Define function to load and preprocess image
    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Hello {name}")
    st.sidebar.header("Navigation")
    if st.sidebar.button('Glaucoma'):
        webbrowser.open_new_tab('https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/glaucoma#:~:text=What%20is%20glaucoma%3F,a%20comprehensive%20dilated%20eye%20exam.')
    if st.sidebar.button('Diabetic Retinopathy'):
        webbrowser.open_new_tab('https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/diabetic-retinopathy#:~:text=Diabetic%20retinopathy%20is%20an%20eye,at%20least%20once%20a%20year.')
    if st.sidebar.button("Cataract"):
        webbrowser.open_new_tab('https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/cataracts#:~:text=A%20cataract%20is%20a%20cloudy,to%20get%20rid%20of%20cataracts.')
    def preprocess_image(image):
        # Load image and resize to expected input shape
        image=image.resize((224,224))
        img_array = img_to_array(image)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.
        return img_array

    # Define function to make predictions on image using custom CNN model
    def predict_custom_cnn(image, model):
        # Preprocess image
        image = preprocess_image(image)
        # Make prediction on image
        predictions = model.predict(image)
        return predictions

    # Define Streamlit app
    def app():
        st.title("Eye disease recognition")
        image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if image_file is not None:
            image = Image.open(image_file)
            st.image(image, caption="Uploaded image", width=400)
            cnn_model_1 = load_model('drgn.h5',compile=False)
            with st.spinner('Making prediction with Custom CNN Model 1...'):
                cnn_model_1_predictions = predict_custom_cnn(image, cnn_model_1)
            st.subheader("Diabetic retinopathy, Glaucoma or Neither")
            #########test code
            ########end test code
            if cnn_model_1_predictions[0][0] > cnn_model_1_predictions[0][1] and cnn_model_1_predictions[0][0] > cnn_model_1_predictions[0][2]:
                st.write('Detecting majority presence of Diabetic Retinopathy')
            elif cnn_model_1_predictions[0][1] > cnn_model_1_predictions[0][0] and cnn_model_1_predictions[0][1] > cnn_model_1_predictions[0][2]:
                st.write('Detecting majority presence of Glaucoma')
            else:
                st.write('The image is classified as Neither')
            cnn_model_2 = load_model('crne.h5',compile=False)
            with st.spinner('Making prediction with Custom CNN Model 2...'):
                cnn_model_2_predictions = predict_custom_cnn(image, cnn_model_2)
            # Display second custom CNN model predictions
            st.subheader("Cataract or Normal")
            if cnn_model_2_predictions[0][0] < 0.5:
                st.write('Not detecting the presence of cataract.')
            else:
                st.write('Detecting the presence of cataract.')
            
            def plotOfValues():
                probabilities = cnn_model_1_predictions[0]

                # Define the labels for the pie chart
                labels = ['Diabetic Retinopathy', 'Glaucoma', 'Normal Eyes']

                # Define the colors for each slice of the pie chart
                colors = ['#ff9999','#66b3ff','#99ff99']

                # Create the pie chart
                plt.pie(probabilities, labels=labels, colors=colors, autopct='%1.1f%%')

                # Add a title to the pie chart
                plt.title('Softmax Output for 3 Classes')

                # Display the pie chart
                st.pyplot(plt)
            plotOfValues()
           

    # Run Streamlit app
    if __name__ == '__main__':
        app()
