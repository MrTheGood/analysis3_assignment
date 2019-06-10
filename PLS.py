import json


class Person:
    def __init__(self, number, first_name, last_name):
        self.number = number
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Costumer(Person):
    def __init__(self, number, first_name, last_name, gender, name_set, street_address, zip_code,
                 city, email_address, user_name, telephone_number):
        super().__init__(number, first_name, last_name)
        self.gender = gender
        self.name_set = name_set
        self.street_address = street_address
        self.zip_code = zip_code
        self.city = city
        self.email_address = email_address
        self.user_name = user_name
        self.telephone_number = telephone_number


class Librarian(Person):
    def __init__(self, number, first_name, last_name):
        super().__init__(number, first_name, last_name)


class Author(Person):
    def __init__(self, number, first_name, last_name):
        super().__init__(number, first_name, last_name)


class Book:
    def __init__(self, author, isbn, country, link, pages, title, year, image_link, language):
        self.author = author
        self.isbn = isbn
        self.country = country
        self.link = link
        self.pages = pages
        self.title = title
        self.year = year
        self.image_link = image_link
        self.language = language


class BookItem:
    def __init__(self, book):
        self.book = book


class LoanItem:

    def __init__(self, book_item, customer):
        self.book_item = book_item
        self.customer = customer


class Library:
    def __init__(self):
        self.librarians = []
        self.catalog = Catalog()
        self.loan_administration = LoanAdministration()

    def enter(self):
        commands = [
            Command("catalog", self.catalog.enter),
            Command("loan_administration", self.loan_administration.enter),
            Command("backup", self.backup),
        ]
        print("What do you want to do?")
        do_command("Library", commands)

    def backup(self):
        commands = [
            Command("restore", self.restore_from_backup),
            Command("create", self.create_backup),
        ]
        print("You chose backup. Do you want to restore or delete??")
        do_command("Library/backup", commands)

    def restore_from_backup(self):
        print("Sorry, not done yet!")

    def create_backup(self):
        print("Creating backup...")
        json.dump(self, open('backup.json', 'w'), default=lambda o: o.__dict__)
        print("Backup done!")
        print("You can find the backup in backup.json")


class LoanAdministration:
    def __init__(self):
        self.loanedItems = []
        self.customers = []

    def enter(self):
        commands = [
            Command("add", self.add_customer),
            Command("add_from_csv", self.load_customers),
            Command("loan_book", self.loan_book),
            Command("show_available_books", self.show_available_books),
        ]
        print("You chose loan_administration. What do you want to do now?")
        do_command("Library/loan_administration", commands)

    def add_customer(self):
        # todo: add customer
        pass

    def load_customers(self):
        # todo: load customers from csv
        pass

    def loan_book(self):
        # todo: loan a book
        pass

    # TODO: take into account loans
    def show_available_books(self):
        book_items = library.catalog.book_items
        known_books = library.catalog.known_books
        print("Available books:", len(book_items))
        for book in known_books:
            book_items = [book_item for book_item in book_items if book_item.book.isbn == book.isbn]
            print("items available for book", book.isbn, book.title, ":", len(book_items))


class Catalog:
    def __init__(self):
        self.book_items = []
        self.known_books = []

    def enter(self):
        print("Welcome to the book catalog. What do you want to do?")
        commands = [
            Command("load_books", self.load_books),
            Command("add_book", self.add_book),
            Command("add_book_item", self.add_book_item),
            Command("show_known_books", self.show_known_books),
            Command("search_books", self.search_books),
        ]
        do_command("Library/catalog", commands)

    # todo: load initial data or whatever
    def load_books(self):
        pass

    def add_book(self):
        print("Please enter all information for the book you want to add:")
        book = Book(
            self.select_author(),
            input("Book isbn: "),
            input("country: "),
            input("link: "),
            input("pages: "),
            input("title: "),
            input("year: "),
            input("image_link: "),
            input("language: ")
        )
        self.known_books.append(book)
        print("Added!")
        return book

    def select_author(self):
        while True:
            authors = {book.author for book in self.known_books}
            print("Available authors:", len(authors))
            print("\n".join([author.get_full_name() for author in authors]))
            name = input("Type the full name of your author:\n")

            for author in authors:
                if name == author.get_full_name():
                    print("You chose", name)
                    return author

            add = input(
                "Author with name " + name + " not found. Do you want to add them? (y/n) ") == "y"
            if add:
                author = Author(input("Give a number for the author: \n"), name.split(" ")[0],
                                " ".join(name.split(" ")[1:]))
                print("You chose", author.get_full_name())
                return author
            print("Try again.")

    def add_book_item(self):
        while True:
            print("Known books:", len(self.known_books))
            print("\n".join([book.title for book in self.known_books]))
            title = input("Type the full title of your book:\n")
            for book in self.known_books:
                if title == book.title:
                    print("You chose ", title)
                    self.book_items.append(BookItem(book))
                    print("A book item has been added.")
                    return book

            add = input(
                "Book with title " + title + " not found. Do you want to add them? (y/n) ") == "y"
            if add:
                book = self.add_book()
                self.book_items.append(BookItem(book))
                print("Added!")
                return book
            print("Try again.")

    def show_known_books(self):
        print("Known books:", len(self.known_books))
        for book in self.known_books:
            print(book.isbn, book.title)

    def search_books(self):
        title = input("Type the title of the book:\n")
        print("Found books:")

        found = False
        for book in self.known_books:
            if title in book.title:
                found = True
                book_items = [book_item for book_item in self.book_items if
                              book_item.book.isbn == book.isbn]
                print(book.isbn + " " + book.title + ", number of copies: " + len(book_items))
        if not found:
            print("No books found.")


class Command:
    def __init__(self, command_name, on_command):
        self.command_name = command_name
        self.on_command = on_command


if __name__ == '__main__':
    library = Library()
    print("Welcome to the HR Library system.")
    library.enter()


    def do_command(current_command, options):
        while True:
            print("You are in " + current_command)
            print("These are your options: back, " +
                  ', '.join([c.command_name for c in options]))
            command = input("type in your choice: \n")
            found = False
            for c in options:
                if command == "back":
                    return
                if c.command_name == command:
                    c.on_command()
                    input("Press enter to continue.\n")
                    found = True
                    break
            if not found:
                print("Invalid option. Try again.")
