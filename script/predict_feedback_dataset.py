# Import the necessary library

import streamlit as st
import pickle
from db_processor import insert_review
from db_processor import query_review
from review_cleaner import prepare_data
from generate_review import get_reviews
import matplotlib.pyplot as plt
import pandas as pd
import re


#Load data(model) from notebook
def load_model():
    with open('model_steps.pkl', 'rb') as file:
        frame = pickle.load(file)
    model = frame['model']
    return model

#Get the id of from the product url
def get_product_id(url):
    if url == "":
        st.write("Enter Product URL ")
        return None
    elif url != "":
        for i in re.findall('[A-Z0-9]+', url):
            if len(i) == 10:
                return i

# Get the dataset and transform to usable format
@st.cache
def get_dataset():
    df = pd.read_csv("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv")
    df['asins'] = df['asins'].astype(str)
    df['asins'] = df['asins'].str.split(',')
    df = df.explode('asins')
    df = df.set_index('asins')
    return df

# Get an object of the dataframe
dataset = get_dataset()

if "dataset" not in st.session_state:
   st.session_state.dataset =  get_dataset()
else:
   dataset = st.session_state.dataset

# Get the reviews of the selected product
@st.cache
def get_reviews_dataset(prod_id):
    reviews = dataset.loc[prod_id]['reviews.text']
    return reviews

# Get a dataframe from predictions
def get_dataframe_from_predictions(prediction):
    if type(prediction) is dict:
        very_happy = prediction["veryHappy"]
        happy = prediction["happy"]
        satisfied = prediction["satisfied"]
        indifferent = prediction["indifferent"]
        disappointed = prediction["disappointed"]
    else:
        very_happy = len(list(filter(lambda pred: pred == "Very Happy", prediction)))
        happy = len(list(filter(lambda pred: pred == "Happy", prediction)))
        satisfied = len(list(filter(lambda pred: pred == "Satisfied", prediction)))
        indifferent = len(list(filter(lambda pred: pred == "Indifferent", prediction)))
        disappointed = len(list(filter(lambda pred: pred == "Disappointed", prediction)))

    prediction_dict = { 'sentiments': ['Very Happy','Happy', 'Satisfied', 'Indifferent', 'Disappointed'],
                        'total': [very_happy, happy, satisfied, indifferent, disappointed]}
    data_frame = pd.DataFrame(prediction_dict)
    return data_frame

# Create the pie chart
def create_pie_chart(df):

    labels = df['sentiments']
    pie_array = df['total']
    plt.pie(pie_array, labels=labels, autopct='%1.1f%%')
    plt.title('Customer Feedback Visualization')
    plt.axis('equal')
    plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.balloons()
    st.pyplot()
    return


# Display visualization of the predictions
def show_result(prediction_df):
    filtered_df = prediction_df[prediction_df['total'] > 0]
    st.table(filtered_df)
    # Create a pie chart with the pie chart function
    create_pie_chart(filtered_df)

# Generates the prediction and visualization for existing dataset
def show_predict_feedback_dataset_page():


    product_url = st.sidebar.text_input("Enter product URL", placeholder='Enter url')
    # Get the product id and corresponding reviews
    try:
        if product_url.strip():
                db_result = query_review(product_url)
                if db_result:
                    prediction_df = get_dataframe_from_predictions(db_result)
                    show_result(prediction_df)
                else:
                    prod_id = get_product_id(product_url)
                    reviews = get_reviews_dataset(prod_id)
                    if prod_id in dataset.index and len(reviews) > 300:
                        get_array = prepare_data(dataset)
                        model = load_model()
                        prediction = model.predict(get_array)
                        prediction_df = get_dataframe_from_predictions(prediction)
                        insert_review(prod_id,product_url,prediction_df["total"][0].item(),prediction_df["total"][1].item(),prediction_df["total"][2].item(),prediction_df["total"][3].item(),prediction_df["total"][4].item() )
                        show_result(prediction_df)
                    else:
                        st.write("Insufficient number of reviews found")
        else:
            st.write("You have not entered your product url")
    # In case of the wrong input
    except Exception as ex:
        st.write(ex)


# Generates the prediction and visualization for real-time data(reviews)
def show_predict_feedback_real_time_page():

    product_url_real = st.sidebar.text_input("Enter product URL", placeholder='Enter url')
    try:
        if product_url_real.strip():
            db_result = query_review(product_url_real)
            if db_result:
                prediction_df = get_dataframe_from_predictions(db_result)
                show_result(prediction_df)
            else:
                reviews_real = get_reviews(product_url_real)
                if product_url_real and len(reviews_real) > 300:
                    get_array = prepare_data(pd.DataFrame(reviews_real, columns=['reviews.text']))
                    classifier = load_model()
                    prediction = classifier.predict(get_array)
                    prediction_df = get_dataframe_from_predictions(prediction)
                    insert_review("",product_url_real, prediction_df["total"][0].item(), prediction_df["total"][1].item(),
                                  prediction_df["total"][2].item(), prediction_df["total"][3].item(), prediction_df["total"][4].item())
                    show_result(prediction_df)

                else:
                    st.write("Insufficient number of reviews found")

        else:
            st.write("You have not entered your product url")
    # In case of the wrong input
    except Exception as ex:
        st.write(ex)