import sqlite3

# conn = sqlite3.connect("Data/ebookstore.db")
conn = sqlite3.connect(":memory:")
db_cursor = conn.cursor() # Get a cursor object

class Book():
    '''A prototype of a book.'''

    def __init__(self, id, title, author, qty):
        '''Initialize book attributes'''

        self.id = id
        self.title = title
        self.author = author
        self.qty = qty

    def __str__(self):
        '''This method returns a string representation of a class.'''

        string_repr = '''Book object:
    ID = {self.id}
    Title = {self.title}
    Author = {self.author}
    Quantity = {self.qty}
    '''

        return string_repr


try:
    db_cursor.execute('''
        CREATE TABLE books (id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
    ''')
    print("Table created")
    conn.commit()

    # Records are initialized by creating multiple instances of the book class
    book_1 = Book(3001, "a tale of two cities", "charles dickens", 30)
    book_2 = Book(3002, "harry potter and the philosopher's stone", "j. k. rowling", 40)
    book_3 = Book(3003, "the lion, the witch and the wardrobe", "c. s. lewis", 25)
    book_4 = Book(3004, "the lord of the rings", "j. r. r. tolkien", 37)
    book_5 = Book(3005, "alice in wonderland", "lewis caroll", 12)
    book_6 = Book(3006, "animal farm", "george orwell", 32)
    book_7 = Book(3007, "the stand", "stephen king", 22)

    book_list = [book_1, book_2, book_3, book_4, book_5, book_6, book_7]

    # Populating books table with the records
    for book in book_list:
        db_cursor.execute('''INSERT INTO books(id, Title, Author, Qty) 
                        VALUES (?, ?, ?, ?)''', (book.id, book.title, book.author, book.qty))
    print("Books inserted")
    conn.commit()

except sqlite3.OperationalError as exp:
    print(exp)


def validate_id(id):
    '''
    This function receive an id, checks if any book in the database has the id
    and returns True if the id exists. Otherwise, it returns False
    '''

    db_cursor.execute('''SELECT 1 FROM books WHERE id = :id_''', {"id_": id})
    bool_value = db_cursor.fetchone()

    if bool_value is not None:
        return True
    else:
        return False


def enter_book():
    '''
    This function will enable a user capture data about a book and create a new
    book record in the database using the data
    '''
    
    # Request and validate id
    while True:
        id = (input("Enter book id: "))
        try:
            id = int(id)
        except ValueError:
            print("Invalid book id entered")
            continue
        
        flag = validate_id(id)
        if  flag == True:
            print("The id already exists")
        else:
            break

    title = input("Enter book title: ").casefold()
    author = input("Enter book author: ").casefold()
    

    # Request and validate quantity
    while True:
        qty = (input("Enter book quantity: "))
        try:
            qty = int(qty)
            break
        except ValueError:
            print("Invalid quantity entered")

    # Create book object
    new_book = Book(id, title, author, qty)

    with conn:
        db_cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                            VALUES (?, ?, ?, ?)''', (new_book.id, new_book.title, new_book.author, new_book.qty))

    print("Book %d added to database" %id)


def update_book():
    '''This function enables a user update information about a book.'''

    while True:
        # Input validation
        while True:
            id = input("Enter the id of the book you want to update: ")
            try:
                id = int(id)
            except ValueError:
                print("The book id must be a number")
                continue
            
            flag = validate_id(id)
            if  flag == True:
                break
            else:
                print("Book id not in database")

        field = input('''Enter the number representing the information you want to update:
        1 - id
        2 - Title
        3 - Author
        4 - Quantity
        0 - Exit
        : ''')

        if field == "1":
            while True:
                new_id = input("Enter the new id: ")
                try:
                    new_id = int(new_id)
                    break
                except ValueError:
                    print("Invalid id entered")
            with conn:
                db_cursor.execute('''UPDATE books SET id = :new_id 
                                    WHERE id = :old_id''', {"new_id": new_id, "old_id": id})
            print("id updated")
            break

        elif field == "2":
            new_title = input("Enter the new title: ").lower()
            with conn:
                db_cursor.execute('''UPDATE books SET Title = :new_title
                                    WHERE id = :id''', {"new_title": new_title, "id": id})
            print("Title updated")
            break

        elif field == "3":
            new_author = input("Enter the new author: ").lower()
            with conn:
                db_cursor.execute('''UPDATE books SET Author = :new_author
                                    WHERE id = :id''', {"new_author": new_author, "id": id})
            print("Author updated")
            break
            
        elif field == "4":
            while True:
                new_qty = input("Enter the new quantity: ")
                try:
                    new_qty = int(new_qty)
                    break
                except ValueError:
                    print("Invalid quantity entered")
            with conn:
                db_cursor.execute('''UPDATE books SET Qty = :new_qty 
                                    WHERE id = :id''', {"new_qty": new_qty, "id": id})
            print("Quantity updated")
            break

        elif field == "0":
            break

        else:
            print("Invalid option")


def delete_book():
    '''This function will enable a user delete a book from the database.'''

    while True:
        book_id = input("Enter the id of the book you want to update: ")
        try:
            book_id = int(book_id)
            break
        except ValueError:
            print("Invalid id entered")

    # Initialize flag
    flag = validate_id(book_id)
    with conn:
        db_cursor.execute('''DELETE FROM books WHERE id = :id_''', {"id_": book_id})

    if  flag == True:
        print("Book %d deleted" %book_id)
    else:
        print("No action taken as no book with the id exists") 


def search_books():
    '''
    This function enables a user search for specific books in the database
    based on the id, title and author. The function then prints the book to the 
    console if the book exists
    '''

    while True:
        field = input('''Select the field you want to base the search on:
        1 - id
        2 - Title
        3 - Author
        0 - Exit
        : ''')

        if field == "1": 
            while True:
                # Validate id type
                book_id = (input("Enter book id: "))
                try:
                    book_id = int(book_id)
                    break
                except ValueError:
                    print("Invalid id entered")

            db_cursor.execute('''SELECT 1 FROM books WHERE id = :id_''', {"id_": book_id})
            flag = db_cursor.fetchone() # Returns one book as each book has a unique id
            if flag is not None:
                db_cursor.execute('''SELECT id, Title, Author, Qty FROM books 
                                    WHERE id = :id_''', {"id_": book_id})
                book_details = db_cursor.fetchone()
                print(book_details)
            else:
                print("No books found")
            break
            
        elif field == "2":
            book_title = input("Enter the book title: ").casefold()
            db_cursor.execute('''SELECT 1 FROM books WHERE title = :title_''', {"title_": book_title})
            flag = db_cursor.fetchall() # Returns many books just in case more than one book shares the same title
            if flag:
                db_cursor.execute('''SELECT id, Title, Author, Qty FROM books
                                    WHERE Title = :title_''', {"title_": book_title})
                book_details = db_cursor.fetchall()
                for row in book_details:
                    print(row)
            else:
                print("No books found")
            break

        elif field == "3":
            book_author = input("Enter the author: ").casefold()
            db_cursor.execute('''SELECT 1 FROM books WHERE Author = :author_''', {"author_": book_author})
            flag = db_cursor.fetchall() # Returns many books just in case more than one book shares the same author
            if flag:
                db_cursor.execute('''SELECT id, Title, Author, Qty FROM books 
                                    WHERE Author = :author_''', {"author_": book_author})
                book_details = db_cursor.fetchall()
                for row in book_details:
                    print(row)
            else:
                print("No books found")
            break

        elif field == "0":
            break

        else:
            print("Invalid option")


def main():
    '''Main function which presents the main menu to the user'''

    while True:
        # presenting the menu to the user.
        menu = input('''Select one of the following options from the menu below:
    1 - Enter book
    2 - Update book
    3 - Delete book
    4 - Search books
    0 - Exit
    : ''')

        if menu == "1":
            enter_book()

        elif menu == "2":
            update_book()

        elif menu == "3":
            delete_book()

        elif menu == "4":
            search_books()

        elif menu == "0":
            break

        else:
            print("Invalid selection")

# Call main.
main()