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

    print("Book added to database")


def update_book():
    '''This function enables a user update information about a book.'''

    while True:
        while True:
            id = input("Enter the id of the book you want to update: ")
            try:
                id = int(id)
                break
            except ValueError:
                print("Invalid id entered")

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