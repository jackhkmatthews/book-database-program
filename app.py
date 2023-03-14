from models import (Base, session, Book, engine)
import time
from typing import List
import datetime
import csv

months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']


def menu():
    while True:
        print('''
              \nProgramming books
              \r1) add book
              \r2) View all books
              \r3) Search for book
              \r4) Book analysis
              \r5) Exit''')
        choice = input('What would you like to do? ')
        if choice in ('1', '2', '3', '4', '5'):
            return choice
        else:
            input('''
                \rPlease choose one of the options above. A number 1-5. Press enter to try again.''')


def clean_date(date_string: str) -> datetime.date:
    try:
        month, day, year = date_string.replace(',', '').split(' ')
        date = datetime.date(int(year), int(months.index(month) + 1), int(day))
    except ValueError:
        input('''
            \n*** Date Error ***
            \rThe date format is wrong
            \rPress enter to try again''')
        return
    else:
        return date


def clean_price(price_str: str) -> float:
    try:
        price = int(float(price_str) * 100)
    except ValueError:
        print('''
            \n*** Price Error ***
            \nPress enter to try agin
        ''')
    else:
        return price


def add_csv():
    with open('suggested_books.csv') as csv_file:
        data = csv.reader(csv_file)
        for row in data:
            title, author, date_str, price_str = row
            book_in_db = session.query(Book).filter(
                Book.title == title).one_or_none()
            if book_in_db == None:
                date = clean_date(date_str)
                price = clean_price(price_str)
                new_book = Book(title=title, author=author,
                                published_date=date, price=price)
                session.add(new_book)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            # add book
            date_error = True
            price_error = True
            title = input('title: ')
            author = input('author: ')
            while date_error:
                date = clean_date(input('date (October 25, 2017): '))
                if type(date) == datetime.date:
                    date_error = False
            while price_error:
                price = clean_price(input('price (12.23): '))
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author,
                            published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book added!')
            time.sleep(1.5)
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        else:
            print('Bye')
            app_running = False
            pass


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()

    for book in session.query(Book):
        print(book)
