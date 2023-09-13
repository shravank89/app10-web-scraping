import requests
import selectorlib
import smtplib
import ssl
import os
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    response = requests.get(url)
    content = response.text
    return content


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def read(tour_info):
    with open("data.txt") as file:
        return file.read()


def store(tour_info):
    with open("data.txt", "a") as file:
        file.write(tour_info + "\n")


def send_email(message):
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
    scraped = scrape(URL)
    extracted = extract(scraped)

    content = read(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(extracted)