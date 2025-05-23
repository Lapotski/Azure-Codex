drop database azuredb;
CREATE DATABASE IF NOT EXISTS AzureDB;
USE AzureDB;

CREATE TABLE Books (
	book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255) NOT NULL,
    total_copies INT NOT NULL,
    available_copies INT NOT NULL
);

CREATE TABLE Members (
	member_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(500) UNIQUE NOT NULL
);

CREATE TABLE BorrowedBooks (
    borrow_id INT PRIMARY KEY AUTO_INCREMENT,
    member INT NOT NULL,
    book INT NOT NULL,
    borrow_date DATE NOT NULL,
    CONSTRAINT fk_member_id FOREIGN KEY (member) REFERENCES Members(member_id),
    CONSTRAINT fk_book_id FOREIGN KEY (book) REFERENCES Books(book_id)
);

INSERT INTO Members (first_name, last_name, age, email) VALUES
  ('Marvi', 'Luna', 28, 'marvi.luna@gmail.com'),
  ('Azure', 'Dan', 34, 'azure.dan@outlook.com'),
  ('Austin', 'Namei', 22, 'austin.namei@gmail.com'),
  ('Mango', 'Angel', 30, 'mango.angel@outlook.com'),
  ('Yu', 'Ace', 40, 'yu.ace@gmail.com'),
  ('Ricardo', 'Taco', 26, 'ricardo.taco@outlook.com'),
  ('Kyla', 'Tato', 45, 'kyla.tato@gmail.com'),
  ('Vi', 'Lane', 31, 'vi.lane@outlook.com'),
  ('Kara', 'Danvers', 38, 'kara.danvers@gmail.com'),
  ('Lena', 'Kieran', 36, 'lena.kieran@outlook.com'),
  ('Austin', 'Johram', 22, 'awst@outlook.com'),
  ('Rio', 'Nico', 22, 'nyeah@outlook.com'),
  ('Airo', 'Nicolai', 27, 'sadiko@outlook.com'),
  ('Vanya', 'Yasha', 38, 'no5@outlook.com');

INSERT INTO Books (title, author, total_copies, available_copies) VALUES
	('A Game of Thrones', 'George R.R. Martin', 8, 8),
	('The Hobbit', 'J.R.R. Tolkien', 12, 12),          
	('Murder on the Orient Express', 'Agatha Christie', 5, 5),
	('The Shining', 'Stephen King', 7, 7),
	('American Gods', 'Neil Gaiman', 6, 6),
	('Gideon the Ninth', 'Tamsyn Muir', 9, 9),
	('Pride and Prejudice', 'Jane Austen', 10, 10),
	('The Cat in the Hat', 'Dr. Seuss', 15, 15),
	('A Clash of Kings', 'George R.R. Martin', 8, 8),
	('The Lord of the Rings: The Fellowship of the Ring', 'J.R.R. Tolkien', 12, 12),
	('The Murder of Roger Ackroyd', 'Agatha Christie', 5, 5),
	('It', 'Stephen King', 7, 7),
	('Good Omens', 'Neil Gaiman', 6, 6),
	('Harrow the Ninth', 'Tamsyn Muir', 10, 10),
	('Sense and Sensibility', 'Jane Austen', 9, 9),
	('Green Eggs and Ham', 'Dr. Seuss', 15, 15),
	('The Winds of Winter', 'George R.R. Martin', 8, 8),
	('The Two Towers', 'J.R.R. Tolkien', 12, 12),
	('And Then There Were None', 'Agatha Christie', 5, 5),
	('Carrie', 'Stephen King', 7, 7),
	('Neverwhere', 'Neil Gaiman', 6, 6),
	('Hop on Pop', 'Dr. Seuss', 12, 12),
	('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 10, 10),
	('Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 10, 10),
	('Harry Potter and the Prisoner of Azkaban', 'J.K. Rowling', 10, 10),
	('Harry Potter and the Goblet of Fire', 'J.K. Rowling', 11, 11),
	('Harry Potter and the Order of the Phoenix', 'J.K. Rowling', 12, 12),
	('Harry Potter and the Half-Blood Prince', 'J.K. Rowling', 12, 12),
	('Harry Potter and the Deathly Hallows', 'J.K. Rowling', 15, 15),
	('Percy Jackson & The Olympians: The Lightning Thief', 'Rick Riordan', 10, 10),
	('Percy Jackson & The Olympians: The Sea of Monsters', 'Rick Riordan', 10, 10),
	('Percy Jackson & The Olympians: The Titan\'s Curse', 'Rick Riordan', 10, 10),
	('Percy Jackson & The Olympians: The Battle of the Labyrinth', 'Rick Riordan', 10, 10),
	('Percy Jackson & The Olympians: The Last Olympian', 'Rick Riordan', 10, 10),
	('The Hunger Games', 'Suzanne Collins', 13, 13),
	('Catching Fire', 'Suzanne Collins', 15, 15), 
	('Mockingjay', 'Suzanne Collins', 16, 16);
    
