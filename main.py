import requests
import selectorlib
import smtplib
import ssl
import os
import sqlite3
import time


URL = "http://programmer100.pythonanywhere.com/tours/"


class Events:
    def scrape(self, url):
        response = requests.get(url)
        content = response.text
        return content

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Database:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    def read(self, tour_info):
        tour_data = tour_info.split(",")
        tour_data = [data.strip() for data in tour_data]
        name, city, date = tour_data

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE name=? AND city=? AND date=?", (name, city, date))
        row = cursor.fetchall()
        return row

    def store(self, tour_info):
        tour_data = tour_info.split(",")
        tour_data = [item.strip() for item in tour_data]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?, ?, ?)", tour_data)
        self.connection.commit()


class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465
        email_sender = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        email_receiver = os.getenv("EMAIL")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as mail_server:
            mail_server.login(email_sender, password)
            mail_server.sendmail(email_sender, email_receiver, message)


if __name__ == "__main__":
    while True:
        event = Events()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)

        if extracted != "No upcoming tours":
            database = Database(db_path="data.db")
            mail = Email()
            data_row = database.read(extracted)
            if not data_row:
                database.store(extracted)
                mail.send(extracted)
        time.sleep(2)
