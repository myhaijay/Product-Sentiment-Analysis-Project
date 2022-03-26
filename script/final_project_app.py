import streamlit as st
st.set_page_config(layout="wide")
from predict_feedback_dataset import show_predict_feedback_dataset_page
from predict_feedback_dataset import show_predict_feedback_real_time_page


#Make a selection box
page = st.sidebar.selectbox("Prediction", ("Select your option","Predict Existing","Predict Real-time"))
st.title("Product Customer Feedback")

st.write("### We need some information to predict Customer feedback")

#Execute the function if selection is made
if page == "Predict Existing":
    show_predict_feedback_dataset_page()
elif page == "Predict Real-time":
    show_predict_feedback_real_time_page()
