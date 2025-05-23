import pymysql
from tkinter import messagebox

# Connect to database
def connect_database():
    try:
        conn = pymysql.connect(host="localhost", user="root", password="root", database="AzureDB")
        return conn, conn.cursor()
    except Exception as e:
        messagebox.showerror('Database Connection Error', f"Something went wrong:\n{e}\nMake sure MySQL is running.")
        return None, None

# Database functions for everything that concerns the members table
class Members:
    def __init__(self, f_name, s_name, age, email, mem_id=None):
        self.f_name = f_name
        self.s_name = s_name
        self.age = age
        self.email = email
        self.mem_id = mem_id

    @classmethod
    def fetch_mems(cls):
        conn, cur = connect_database()
        if conn is None or cur is None:
            return []

        try:
            cur.execute("SELECT * FROM members")
            return cur.fetchall()
        finally:
            conn.close()

    @classmethod
    def search_members(cls, option, val):
        column_map = {
            "ID": "member_id",
            "First Name": "first_name",
            "Last Name": "last_name",
            "Age": "age",
            "Email": "email"
        }

        db_column = column_map.get(option)
        if not db_column:
            raise ValueError(f"Invalid search option: {option}")

        conn, cur = connect_database()
        if conn is None or cur is None:
            return []

        try:
            cur.execute(f"SELECT * FROM members WHERE LOWER({db_column}) LIKE LOWER(%s)", (f"%{val}%",))
            return cur.fetchall()
        finally:
            conn.close()

    def add_members(self):
        conn, cur = connect_database()
        if conn is None or cur is None:
            return

        try:
            cur.execute(
                "INSERT INTO members (first_name, last_name, age, email) VALUES (%s, %s, %s, %s)",
                (self.f_name, self.s_name, self.age, self.email)
            )
            conn.commit()
        finally:
            conn.close()

    def update_members(self):
        conn, cur = connect_database()
        if conn is None or cur is None:
            return

        try:
            cur.execute(
                "UPDATE members SET first_name=%s, last_name=%s, age=%s, email=%s WHERE member_id=%s",
                (self.f_name, self.s_name, self.age, self.email, self.mem_id)
            )
            conn.commit()
        finally:
            conn.close()

    def delete_members(self):
        conn, cur = connect_database()
        if conn is None or cur is None:
            return

        try:
            cur.execute("DELETE FROM members WHERE member_id=%s", (self.mem_id,))
            conn.commit()
        finally:
            conn.close()

# Database functions for everything that concerns the books table
class Books:
    def __init__(self, title, author, total, available, book_id=None):
        self.title = title
        self.author = author
        self.total = total
        self.available = available
        self.book_id = book_id

    @classmethod
    def fetch_books(cls):
        conn, cur = connect_database()
        if conn is None or cur is None:
            return []

        try:
            cur.execute("SELECT * FROM books")
            return cur.fetchall()
        finally:
            conn.close()

    @classmethod
    def search_books(cls, option, val):
        column_map = {
            "ID": "book_id",
            "Title": "title",
            "Author": "author",
        }

        db_column = column_map.get(option)
        if not db_column:
            raise ValueError(f"Invalid search option: {option}")

        conn, cur = connect_database()
        if conn is None or cur is None:
            return []

        try:
            cur.execute(f"SELECT * FROM books WHERE LOWER({db_column}) LIKE LOWER(%s)", (f"%{val}%",))
            return cur.fetchall()
        finally:
            conn.close()

    def add_books(self):
        conn, cur = connect_database()
        if conn is None or cur is None:
            return

        try:
            cur.execute(
                "INSERT INTO books (title, author, total_copies, available_copies) VALUES (%s, %s, %s, %s)",
                (self.title, self.author, self.total, self.available)
            )
            conn.commit()
        finally:
            conn.close()

    def update_books(self):
        conn, cur = connect_database()
        if conn is None or cur is None:
            return

        try:
            cur.execute(
                "UPDATE books SET title=%s, author=%s, total_copies=%s, available_copies=%s WHERE book_id=%s",
                (self.title, self.author, self.total, self.available, self.book_id)
            )
            conn.commit()
        finally:
            conn.close()

    def delete_books(self):
        conn, cur = connect_database()
        if conn is None or cur is None:
            return

        try:
            cur.execute("DELETE FROM books WHERE book_id=%s", (self.book_id,))
            conn.commit()
        finally:
            conn.close()

# Database functions for everything that concerns the borrowedbooks table
class BorrowedBooks:
    def __init__(self, member, book, borrow_date, borrow_id=None):
        self.member = member
        self.book = book
        self.borrow_date = borrow_date
        self.borrow_id = borrow_id
        
    @classmethod
    def fetch_bBooks(cls):
        conn, cur = connect_database()
        if conn is None or cur is None:
            return []

        try:
            cur.execute("""
                        SELECT 
                        bb.borrow_id,
                        CONCAT(m.first_name, ' ', m.last_name) AS member_name,
                        b.title AS book_title,
                        bb.borrow_date
                        FROM BorrowedBooks bb
                        JOIN Members m ON bb.member = m.member_id
                        JOIN Books b ON bb.book = b.book_id;
                        """)
            return cur.fetchall()
        finally:
            conn.close()

    @classmethod
    def search_bBooks(cls, option, val):
        column_map = {
            "ID": "bb.borrow_id",
            "Member": "CONCAT(m.first_name, ' ', m.last_name)",
            "Book": "b.title"
        }

        db_column = column_map.get(option)
        if not db_column:
            raise ValueError(f"Invalid search option: {option}")

        conn, cur = connect_database()
        if conn is None or cur is None:
            return []

        try:
            query = f"""
                SELECT 
                    bb.borrow_id,
                    CONCAT(m.first_name, ' ', m.last_name) AS member_name,
                    b.title AS book_title,
                    bb.borrow_date
                FROM BorrowedBooks bb
                JOIN Members m ON bb.member = m.member_id
                JOIN Books b ON bb.book = b.book_id
                WHERE LOWER({db_column}) LIKE LOWER(%s)
            """
            cur.execute(query, (f"%{val}%",))
            return cur.fetchall()
        finally:
            conn.close()

    def issue_book(self):
        conn, cur = connect_database()
        if conn is None or cur is None:
            return

        try:
            cur.execute(
                "INSERT INTO borrowedbooks (member, book, borrow_date) VALUES (%s, %s, %s)",
                (self.member, self.book, self.borrow_date)
            )

            cur.execute(
                "UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = %s AND available_copies > 0",
                (self.book,)
            )
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            print(f"Error issuing book: {e}")
        finally:
            conn.close()

    def return_bBook(self):
        if not getattr(self, "borrow_id", None):
            print("No borrow_id set – nothing to return.")
            return

        conn, cur = connect_database()
        if conn is None or cur is None:
            return

        try:
            cur.execute(
                "SELECT book FROM borrowedbooks WHERE borrow_id = %s",
                (self.borrow_id,)
            )
            row = cur.fetchone()
            if not row:
                print(f"Borrow record {self.borrow_id} not found.")
                return

            book_id = row[0]
            print(book_id)

            cur.execute(
                "UPDATE Books "
                "SET available_copies = available_copies + 1 "
                "WHERE book_id = %s",
                (book_id,)
            )
            if cur.rowcount == 0:
                conn.rollback()
                print(f"UPDATE failed – book_id {book_id} not found in Books.")
                return

            cur.execute(
                "DELETE FROM borrowedbooks WHERE borrow_id = %s",
                (self.borrow_id,)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"Error returning book: {e}")

        finally:
            conn.close()


