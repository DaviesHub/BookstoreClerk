import sqlite3

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


# conn = sqlite3.connect("Data/ebookstore.db")
conn = sqlite3.connect(":memory:")
db_cursor = conn.cursor() # Get a cursor object

db_cursor.execute('''
    CREATE TABLE books id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER
''')
conn.commit()

# Records are initialized by creating multiple instances of the book class
book_1 = Book(3001, "A Tale of Two Cities", "Charles Dickens", 30)
book_2 = Book(3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40)
book_3 = Book(3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25)
book_4 = Book(3004, "The Lord of the Rings", "J. R. R. Tolkien", 37)
book_5 = Book(3005, "Alice in Wonderland", "Lewis Caroll", 12)
book_6 = Book(3006, "Animal Farm", "George Orwell", 32)
book_7 = Book(3007, "The Stand", "Stephen King", 22)




# Create functions to 

# Add new books

# Update book information

# Delete books

# Search database to find books