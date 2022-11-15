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

# Initialize records



# Create functions to 

# Add new books

# Update book information

# Delete books

# Search database to find books