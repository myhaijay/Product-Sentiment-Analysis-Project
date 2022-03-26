from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import nltk
import re

def clean_text(text):
    stopwords = nltk.corpus.stopwords.words('english')
    wn = nltk.WordNetLemmatizer()
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [wn.lemmatize(word) for word in tokens if word not in stopwords]
    return text
    
def prepare_data(data_frame):
    tfidf_vector = TfidfVectorizer(analyzer=clean_text, ngram_range=(1, 5), sublinear_tf=True)
    #print(data_frame)
    X_tfidf = tfidf_vector.fit_transform(data_frame['reviews.text'])
    df_array = X_tfidf.toarray()
    svd = TruncatedSVD(n_components=300)
    svd.fit(df_array)
    df_array_transformed2 = svd.fit_transform(df_array)
    return df_array_transformed2