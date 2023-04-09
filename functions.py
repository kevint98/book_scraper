import requests
import random
import os
import smtplib
import ssl
from bs4 import BeautifulSoup
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

import datetime

date_time = datetime.datetime.now()
# from email import contentmanager


def get_genres(url):
    # Excluding genres according to taste and
    # excluding ebooks per Goodreads robot.txt
    unwanted_genres = ['Chick Lit', "Children's",
                       'Comics', 'Cookbooks', 'Ebooks', 'Manga']

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    genres = set()

    for genre in soup.select('.bigBoxBody .gr-hyperlink'):
        genres.add(genre.get_text())  # Only add unique genres on the page

    genre_list = list(genres)
    genre_list.sort()

    for unwanted_genre in unwanted_genres:
        if unwanted_genre in genre_list:
            genre_list.remove(unwanted_genre)

    return genre_list


def get_books_by_genre(genre):

    page = random.randint(1, 26)
    url = 'https://www.goodreads.com/shelf/show/{}?page={}'.format(
        genre, page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    books = []
    raw_books = soup.select('.elementList')
    random.shuffle(raw_books)

    for book in raw_books:
        if len(book.select('.bookTitle')) != 0:
            title = book.select('.bookTitle')[0].get_text()
            author = book.select('.authorName')[0].get_text()
            books.append(title + ' by ' + author)

            if len(books) == 5:
                break

    return books

def send_recommendations(filename, date):

    from_addr = os.environ.get('OUTLOOK_EMAIL')
    to_addr = os.environ.get('OUTLOOK_EMAIL')
    password = os.environ.get('OUTLOOK_SMTP_PASS')

    body = 'These are your book recommendations for the next month.\n\nRemember to add your chosen books to your bookshelf.'

    msg = MIMEMultipart()
    msg['Subject'] = f'Book Recommendations for {date}'
    msg['To'] = to_addr
    msg['From'] = from_addr
    body = MIMEText(body, 'plain')
    msg.attach(body)

    with open(filename, 'r') as f:
        part = MIMEApplication(f.read(), 'octet-stream')
        part['Content-Disposition'] = f"attachment; filename= {filename}"
    msg.attach(part)

    with smtplib.SMTP('smtp-mail.outlook.com') as server:
        server.ehlo()
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
