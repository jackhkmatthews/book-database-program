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


def submenu():
    while True:
        print('''
              \nProgramming books
              \r1) Edit
              \r2) Delete
              \r3) Exit''')
        choice = input('What would you like to do? ')
        if choice in ('1', '2', '3'):
            return choice
        else:
            input('''
                \rPlease choose one of the options above. A number 1-3. Press enter to try again.''')


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


def clean_id(id: str, id_options: List[int]) -> int:
    try:
        book_id = int(id)
    except ValueError:
        input('''
        \n*** ID Error ***
        \rId should be a number
        \rPress enter to try agin
        ''')
        return
    else:
        if book_id in id_options:
            return book_id
        else:
            input('''
            \n*** ID Error ***
            \rId should one of the options
            \rPress enter to try agin
            ''')


def edit_check(column_name: str, current_value):
    print(f'\n*** Edit {column_name} **')
    if column_name == 'Price':
        print(f'\rCurrent value: {current_value/100}')
    elif column_name == 'Date':
        print(f'\rCurrent value: {current_value.strftime("%B %d %Y")}')
    else:
        print(f'\rCurrent value: {current_value}')

    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            if column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to? ')


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
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} | {book.price}')
            input('\nPress enter to return to menu')
            pass
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = clean_id(input(f'''
                    \nId options: {id_options}
                    \rBook id: '''), id_options)
                if type(id_choice) == int:
                    id_error = False
            book = session.query(Book).filter(Book.id == id_choice).first()
            print(f'{book.id} | {book.title} | {book.author} | {book.price / 100}')
            sub_choice = submenu()
            if sub_choice == '1':
                book.title = edit_check('Title', book.title)
                book.author = edit_check('Author', book.author)
                book.published_date = edit_check(
                    'Date', book.published_date)
                book.price = edit_check('Price', book.price)
                session.commit()
                print('Book updated!')
                time.sleep(1.5)
            if sub_choice == '2':
                session.delete(book)
                session.commit()
                print('Book deleted!')
                time.sleep(1.5)
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
