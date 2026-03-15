from flask import Flask
import mysql.connector
import time

app = Flask(__name__)

@app.route("/")
def home():
    try:
        conn = mysql.connector.connect(
            host="mysql_db",
            user="root",
            password="root",
            database="testdb"
        )
        return "Connected to MySQL successfully!"
    except:
        return "Database connection failed!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

