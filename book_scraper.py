from functions import *
import datetime

date_time = datetime.datetime.now()
date_time_formatted = date_time.strftime('%a %b %d %Y %X')

text_file = f'book_recommendations_{date_time.date()}.txt'

genres = get_genres('https://www.goodreads.com/genres')


with open(text_file, 'a+') as f:
    f.write(f'----------------------\n'
            f'Scraped On: {date_time_formatted}\n')

for genre in genres:

    books = get_books_by_genre(genre)

    with open(text_file, 'a+') as f:
        f.write(f'\nGENRE: {genre.upper()}\n')

    for book in books:
        with open(text_file, 'a+') as f:
            f.write('\t' + book + '\n')
