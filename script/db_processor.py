# Import the necessary library
import mysql.connector
#Establish connection to the database
sqldb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Aijay  gr8",
  database="final_project_db"
)
# Create cursor for row selection in database
sqlcursor = sqldb.cursor(buffered=True)

# Insert result from model prediction into the database
def insert_review(productId, productUrl, veryHappy, happy, satisfied, indifferent,disappointed):   
    sql = """INSERT INTO reviews_sentiment (product_id, product_url,very_happy,happy,satisfied,indifferent,disappointed )
    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    val = (productId, productUrl, veryHappy,happy,satisfied,indifferent,disappointed)
    sqlcursor.execute(sql, val)
    sqldb.commit()

# Query the database for prediction of products
def query_review(product_id_or_url):
    sql = """SELECT * FROM reviews_sentiment WHERE product_id = %s OR product_url = %s"""
    val = (product_id_or_url,product_id_or_url)

    sqlcursor.execute(sql, val)
    result = sqlcursor.fetchone()
    if result:
        return {"veryHappy":result[3], "happy":result[4], "satisfied":result[5], "indifferent":result[6],"disappointed":result[7]}