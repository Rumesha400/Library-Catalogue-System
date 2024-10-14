import os.path
import matplotlib.pyplot as plt
import pandas as pd

# Define the filename for storing the Section data
SECTION_FILE = "section_data.txt"

# Load Section data from file
def load_section_data():
    if os.path.exists(SECTION_FILE):
        with open(SECTION_FILE, "r") as file:
            return file.read().splitlines()
    else:
        return []

# Save Section data to file
def save_section_data():
    with open(SECTION_FILE, "w") as file:
        for section in Section:
            file.write(section + "\n")

# Load Section data from file at startup
Section = load_section_data()

class PasswordFormatError(Exception):
    def __init__(self,arg):
        self.msg=arg
        
class InvalidGenreError(Exception):
    def __init__(self,arg):
        self.msg=arg

class Book:
    # Class variable to store created books
    created_books = []

    def __init__(self, title, author, section_index):
        try:
            if not title:
                raise ValueError("Title cannot be empty.")
            if not author:
                raise ValueError("Author cannot be empty.")
            if section_index < 0 or section_index >= len(Section):
                raise ValueError("Invalid section index.")

            # Additional logic for duplicate validation
            if self.is_duplicate(title, author):
                raise ValueError("This book already exists.")

            self.title = title
            self.author = author
            self.section = Section[section_index]

            # Add the book to the list of created books
            self.created_books.append(self)
        except Exception as e:
            print(e)
    
    @classmethod
    def is_duplicate(cls, title, author):
        # Check if a book with the same title and author already exists
        return any(book.title == title and book.author == author for book in cls.created_books)


    @classmethod
    def delete_book_by_name(cls, book_name, filename):
        while True:
            deleted = False
            with open(filename, 'r') as file:
                lines = file.readlines()
            with open(filename, 'w') as file:
                for line in lines:
                    if book_name in line:
                        deleted = True
                        continue  # Skip writing this line if it matches the book name
                    file.write(line)
            if not deleted:
                print(f"Book '{book_name}' not found in the list.")
            else:
                print(f"Book '{book_name}' deleted successfully.")
                # Update created_books list after deletion
                cls.created_books = [book for book in cls.created_books if book.title != book_name]
                # Save books to file after deletion
                cls.save_books_to_file(filename)
            if not input("Do you want to delete another book? (yes/no): ").lower().strip().startswith('y'):
                break

    @classmethod
    def add_book(cls, title, author, section_index, filename):
        if cls.is_duplicate(title, author):
            print("This book already exists.")
            return

        while True:
            if title == "":
                title = input("The title can not be empty. Enter the Title")
            if author == "":
                author = input("The Author can not be empty. Enter the Author")
            if section_index == None:
                print("Current Sections:", Section)
                section_index = input("The Section can not be empty. Enter the Section")
                try:
                    section_index = int(section_index)
                except ValueError:
                    print("Invalid section index. Please enter a valid integer.")
                    continue

            try:
                if not title:
                    raise ValueError("Title cannot be empty.")
                if not author:
                    raise ValueError("Author cannot be empty.")
                if section_index < 0 or section_index >= len(Section):
                    raise ValueError("Invalid section index.")

                # Check for duplicates before creating the new book object
                if cls.is_duplicate(title, author):
                    print("This book already exists.")
                    break

                # Create a new book object
                new_book = Book(title, author, section_index)

                # Add the new book to the list of created books
                cls.created_books.append(new_book)
                # Save books to file after addition
                cls.save_books_to_file(filename)
                # Print book information
                # Print book information
                print("Book added successfully:")
                print(f" Title: {new_book.title}, Author: {new_book.author}, Section: {new_book.section}")
                
             

                title = None
                author = None
                section_index = None
                break
            except ValueError as e:
                print(f"Error: {e}")
                break





    @classmethod
    def save_books_to_file(cls, filename):
        existing_books = set()
        # Check if the file is empty to determine whether to write the header
        with open(filename, 'r') as file:
            if not file.read(1):  # Check if the file is empty
                with open(filename, 'a') as new_file:
                    new_file.write("Title,Author,Genre\n")  # Write the header row

        # Populate existing_books set with existing entries
        with open(filename, 'r') as file:
            next(file)  # Skip the header row
            for line in file:
                title, author, section = line.strip().split(',')
                existing_books.add((title, author))

        # Append new books to the file
        with open(filename, 'a') as file:
            for book in cls.created_books:
                # Check if the book is not already in the file
                if (book.title, book.author) not in existing_books:
                    file.write(f"{book.title},{book.author},{book.section}\n")
                    existing_books.add((book.title, book.author))


                
    @classmethod
    def Print_Books(cls, filename):
        try:
            with open(filename, 'r') as file:
                # Skip the header row
                next(file)
                print("List of Books:")
                for index, line in enumerate(file, start=1):
                    title, author, section = line.strip().split(',')
                    print(f"{index}. Title: {title}, Author: {author}, Section: {section}")
        except FileNotFoundError:
            print("No books found.")


        

# Check if the password has a special character
def contains_special_character(text):
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    for char in text:
        if char in special_characters:
            return True
    return False

# Check if the password is valid or not
'''
1) Length: 8 characters
2) Only one special character
3) At least one number
4) At least one upper case character
'''
def is_valid_password(password):
    # Password should be at least 8 characters long
    if len(password) < 8:
        return False

    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)

    if not (has_uppercase and has_lowercase and has_digit and contains_special_character(password)):
        return False

    return True

def Login():
    # Defult password
    Password = "Ad123@mi"
    
    # Check inputted password
    password = input("Enter the Password: ")
    print("-----------------------------------------------------------------------")
    if is_valid_password(password):
        if password == Password:
            print("-------------------------- Successful Login --------------------------")
            return True
        else:
            print("-------------------------- Password is incorrect --------------------------")
            return False
    else:
        raise PasswordFormatError('Password should be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit')
        print("-----------------------------------------------------------------------")
        
def Add_Genre():
    def add_genre():
        while True:
            print("Current Sections:", Section)
            user_input = input("Enter the genre you want to add (type 'exit' to stop): ").strip()

            if user_input.lower() == 'exit':
                break

            try:
                if not user_input:
                    raise InvalidGenreError("Genre cannot be empty.")
                elif user_input in Section:
                    raise InvalidGenreError("Genre already exists. Please enter a different genre.")
                else:
                    Section.append(user_input)
                    print(f"Genre '{user_input}' added successfully.")
                    # Save Section data to file after adding a new genre
                    save_section_data()
            except InvalidGenreError as e:
                print(f"Error: {e}")

    try:
        add_genre()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        print("Final List of Sections:", Section)

def execute_class_function():
    while True:
        # Dynamically ask the user which function to call inside the class
        function_name = input("Enter the name of the function to call (e.g., Add_Book, Delete_Book, Print_Books, exit to stop): ")

        if function_name == "Add_Book":
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            print("Current Sections:", Section)
            section_index = int(input("Enter the index of the section: "))
            Book.add_book(title, author, section_index, "books.txt")

        elif function_name == "Delete_Book":
            book_name = input("Enter the title of the book to delete (type 'exit' to stop): ")
            if book_name.lower() == 'exit':
                break
            Book.delete_book_by_name(book_name, "books.txt")

        elif function_name == "Print_Books":
            Book.Print_Books(r'books.txt')

        elif function_name.lower() == 'exit':
            break

        else:
            print("Invalid function name.")

        # Save Section data to file after each function call
        save_section_data()
        

def plot_author_vs_title(filename):
    try:
        # Load data from the inventory file into a DataFrame
        df = pd.read_csv(filename)

        # Group books by author and count the number of titles by each author
        author_counts = df['Author'].value_counts()

        # Group books by title and count the number of occurrences for each title
        title_counts = df['Title'].value_counts()

        # Create subplots
        plt.figure(figsize=(30, 12))

        # Bar plot for Author vs Title
        plt.subplot(1, 3, 1)
        plt.bar(author_counts.index[:10], author_counts.values[:10], color='pink')
        plt.xlabel('Author', fontsize=20)
        plt.ylabel('Number of Titles', fontsize=20)
        plt.title('Titles by Number of Occurrences', fontsize=24)
        plt.xticks(rotation=45, fontsize=18)
        plt.yticks(fontsize=18)

        # Pie chart for Author vs Title
        plt.subplot(1, 3, 2)
        plt.pie(title_counts[:10], labels=title_counts.index[:10], autopct='%1.1f%%', startangle=140, textprops={'fontsize': 18})
        plt.axis('equal')
        plt.title('Titles by Number of Occurrences', fontsize=24)

        # Line plot for Author vs Title
        plt.subplot(1, 3, 3)
        title_counts.plot(marker='o')
        plt.xlabel('Title', fontsize=20)
        plt.ylabel('Number of Occurrences', fontsize=20)
        plt.title('Number of Occurrences for Each Title', fontsize=24)
        plt.grid(True)
        plt.xticks(rotation=45, fontsize=18)
        plt.yticks(fontsize=18)

        # Adjust layout
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("Inventory file not found.")


def plot_books_inventory(filename):
    try:
        # Load data from the inventory file into a DataFrame
        df = pd.read_csv(filename)

        # Group books by genre and count the number of books in each genre
        genre_counts = df.groupby('Genre').size()

        plt.figure(figsize=(18, 6))


        # Bar plot
        plt.subplot(1,3,1)  # 3 rows, 1 column, plot 1
        plt.bar(genre_counts.index, genre_counts.values, color='pink')
        plt.xlabel('Genre')
        plt.ylabel('Number of Books')
        plt.title('Inventory Distribution by Genre')
        plt.xticks(rotation=45)

        # Pie chart
        plt.subplot(1,3,2)  # 3 rows, 1 column, plot 2
        plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Genre Distribution of Inventory')

        # Line plot
        plt.subplot(1,3,3)  # 3 rows, 1 column, plot 3
        genre_counts.plot(marker='o')
        plt.xlabel('Genre')
        plt.ylabel('Number of Books')
        plt.title('Inventory Distribution by Genre')
        plt.grid(True)
        plt.xticks(rotation=45)

        # Adjust layout
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("Inventory file not found.")

def Plots():
    print("Menue:\n1.Title VS Genre\n2.Title VS Author\n3.Exit")
    choice = int(input("Enter the number from the menue that you want to do: "))
    print("-----------------------------------------------------------------------")
    if(choice == 1):
        plot_books_inventory('books.txt')
        Plots()
    elif(choice == 2):
        plot_author_vs_title('books.txt')
        Plots()
    elif(choice == 3):
         pass
        
def Menue():
    print("Menue:\n1.Add Section\n2.Seeing and updating The inventory\n3.Seeing Plots\n4.Exit")
    choice = int(input("Enter the number from the menue that you want to do: "))
    print("-----------------------------------------------------------------------")
    if(choice == 1):
        Add_Genre()
        Menue()
    elif(choice == 2):
        execute_class_function()
        Menue()
    elif(choice == 3):
        Plots()
        Menue()
    elif(choice == 4):
         pass