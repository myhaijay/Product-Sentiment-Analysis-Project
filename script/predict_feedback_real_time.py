import streamlit as st
import predict_feedback_dataset as pf
from generate_review import get_reviews
import pickle
from review_cleaner import prepare_data
import matplotlib.pyplot as plt
import pandas as pd



def load_model():
    with open('model_steps.pkl', 'rb') as file:
        frame = pickle.load(file)
    classifier = frame['model']
    return classifier
model = pf.load_model()


if "data" not in st.session_state:
   st.session_state.data =  pf.get_dataset()
else:
   data = st.session_state.data


def show_predict_feedback_real_time_page():
    st.title("Product Customer Feedback Real-time")

    st.write("### We need some information to predict Customer feedback")

    product_url_real = st.sidebar.text_input("Enter product URL", placeholder='Enter url')
    try:
        reviews_real = get_reviews(product_url_real)
    except ValueError:
        st.write("You have not entered your product url")
    else:
        if product_url_real and len(reviews_real) > 300:
            get_array = prepare_data(pd.DataFrame(reviews_real,columns=['reviews.text']))
            classifier = load_model()
            prediction = classifier.predict(get_array)
            very_happy = len(list(filter(lambda pred: pred == "Very Happy", prediction)))
            happy = len(list(filter(lambda pred: pred == "Happy", prediction)))
            satisfied = len(list(filter(lambda pred: pred == "Satisfied", prediction)))
            indifferent = len(list(filter(lambda pred: pred == "Indifferent", prediction)))
            disappointed = len(list(filter(lambda pred: pred == "Disappointed", prediction)))

            pred_dict = {"Very Happy": [very_happy],
                         "Happy": [happy],
                         "Satisfied": [satisfied],
                         "Indifferent": [indifferent],
                         "Disappointed": [disappointed]}

            pred_df = pd.DataFrame(pred_dict)

            st.table(pred_df)

            pie_array = [very_happy,happy,satisfied,indifferent,disappointed]
            labels = 'Very Happy', 'Happy', 'Satisfied', 'Indifferent', 'Disappointed'
            plt.pie(pie_array, labels=labels, autopct='%1.1f%%')
            plt.title('Customer Feedback Visualization')
            plt.axis('equal')
            plt.show()
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.balloons()
            st.pyplot()
