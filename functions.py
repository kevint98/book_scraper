import requests
from bs4 import BeautifulSoup
import random


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

    page =  random.randint(1, 26)
    url = 'https://www.goodreads.com/shelf/show/{}?page={}'.format(
        genre, page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    books = []
    raw_books = soup.select('.elementList')
    random.shuffle(raw_books)


    for book in raw_books :
        if len(book.select('.bookTitle')) != 0:
            title = book.select('.bookTitle')[0].get_text()
            author = book.select('.authorName')[0].get_text()
            books.append(title + ' by ' + author)
            
            if len(books) == 5:
                break
                         
    return books