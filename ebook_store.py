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
    book_1 = Book(3001, "A Tale of Two Cities", "Charles Dickens", 30)
    book_2 = Book(3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40)
    book_3 = Book(3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25)
    book_4 = Book(3004, "The Lord of the Rings", "J. R. R. Tolkien", 37)
    book_5 = Book(3005, "Alice in Wonderland", "Lewis Caroll", 12)
    book_6 = Book(3006, "Animal Farm", "George Orwell", 32)
    book_7 = Book(3007, "The Stand", "Stephen King", 22)

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

    if bool_value == 1:
        return True
    else:
        return False


def enter_book():
    '''
    This function will enable a user capture data about a book and create a new
    book record in the database using the data
    '''
    
    id = (input("Enter book id: "))
    title = input("Enter book title: ").title()
    author = input("Enter book author: ").title()
    qty = (input("Enter book quantity: "))

    try:
        id = int(id)
    except ValueError:
        print("Invalid book id entered")

    try:
        qty = int(qty)
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
                    new_id = int(id)
                    break
                except ValueError:
                    print("Invalid id entered")
            with conn:
                db_cursor.execute('''UPDATE books SET id = :new_id 
                                    WHERE id = :old_id''', {"new_id": new_id, "old_id": id})
            break

        elif field == "2":
            new_title = input("Enter the new title: ").title()
            with conn:
                db_cursor.execute('''UPDATE books SET Title = :new_title
                                    WHERE id = :id''', {"new_title": new_title, "id": id})
            break

        elif field == "3":
            new_author = input("Enter the new author").title()
            with conn:
                db_cursor.execute('''UPDATE books SET Author = :new_author
                                    WHERE id = :id''', {"new_author": new_author, "id": id})
            break

        elif field == "4":
            new_qty = input("Enter the new quantity: ")
            try:
                new_qty = int(new_qty)
                break
            except ValueError:
                print("Invalid quantity entered")
            with conn:
                db_cursor.execute('''UPDATE books SET Qty = :new_qty 
                                    WHERE id = :id''', {"new_qty": new_qty, "id": id})
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
            book_id = int(id)
            break
        except ValueError:
            print("Invalid id entered")

    # Initialize flag
    flag = validate_id(id)
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
            book_id = input("Enter the book id: ")
            db_cursor.execute('''SELECT 1 FROM books WHERE id = :id_''', {"id_": book_id})
            flag = db_cursor.fetchone() # Returns one book as each book has a unique id
            if flag[0] == 1:
                db_cursor.execute('''SELECT id, Title, Author, Qty FROM books 
                                    WHERE id = :id_''', {"id_": book_id})
                book_details = db_cursor.fetchone()
                print(book_details)
            else:
                print("No books found")
            break
            
        elif field == "2":
            book_title = input("Enter the book title: ").title()
            db_cursor.execute('''SELECT 1 FROM books WHERE title = :title_''', {"title_": book_title})
            flag = db_cursor.fetchall() # Returns many books just in case more than one book shares the same title
            if flag[0][0] == 1:
                db_cursor.execute('''SELECT id, Title, Author, Qty FROM books
                                    WHERE Title = :title_''', {"title_": book_title})
                book_details = db_cursor.fetchall()
                for row in book_details:
                    print(row)
            else:
                print("No books found")
            break

        elif field == "3":
            book_author = input("Enter the new author").title()
            db_cursor.execute('''SELECT 1 FROM books WHERE Author = :author_''', {"author_": book_author})
            flag = db_cursor.fetchall() # Returns many books just in case more than one book shares the same author
            if flag[0][0] == 1:
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