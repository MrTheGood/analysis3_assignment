import json


class Person:
    def __init__(self, number, firstName, lastName):
        self.number = number
        self.firstName = firstName
        self.lastName = lastName

    def getFullName(self):
        return self.firstName + " " + self.lastName


class Costumer(Person):
    def __init__(self, number, firstName, lastName, gender, nameSet, streetAddress, zipCode, city,
                 emailAddress, userName, telephoneNumber):
        super().__init__(number, firstName, lastName)
        self.gender = gender
        self.nameSet = nameSet
        self.streetAddress = streetAddress
        self.zipCode = zipCode
        self.city = city
        self.emailAddress = emailAddress
        self.userName = userName
        self.telephoneNumber = telephoneNumber


class Libarian(Person):
    def __init__(self, number, firstName, lastName):
        super().__init__(number, firstName, lastName)


class Author(Person):
    def __init__(self, number, firstName, lastName):
        super().__init__(number, firstName, lastName)


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
        self.customers = []
        self.librarians = []
        self.catalog = Catalog()
        self.loanAdministration = LoanAdministration()

    def add_customer(self, customer):
        self.customers.append(customer)

    def add_book_item(self, book):
        self.catalog.bookItems.append(BookItem(book))

    def loan_book(self, bookItem, customer):
        if self.catalog.bookItems.__contains__(bookItem):
            self.catalog.bookItems.remove(bookItem)
            self.loanAdministration.loanedItems.append(LoanItem(bookItem, customer))

    def return_book(self, loanItem):
        if self.loanAdministration.loanedItems.__contains__(loanItem):
            self.loanAdministration.loanedItems.remove(loanItem)
            self.catalog.bookItems.append(loanItem.book_item)

    def restore_from_backup(self):
        print("Sorry, not done yet!")

    def create_backup(self):
        print("Creating backup...")
        json.dump(self, open('backup.json', 'w'), default=lambda o: o.__dict__)
        print("Backup done!")


class LoanAdministration:
    def __init__(self):
        self.loanedItems = []


class Catalog:
    def __init__(self):
        self.bookItems = []
        self.knownBooks = []

    def enter(self):
        print("Welcome to the book catalog. What do you want to do?")
        commands = [
            Command("add_book", self.add_book),
            Command("add_book_item", self.add_book_item),
            Command("show_known_books", self.show_known_books),
            Command("show_available_books", self.show_available_books),
            Command("search_books", self.search_books),
        ]
        do_command(commands)

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
        self.knownBooks.append(book)
        print("Added!")
        return book

    def add_book_item(self):
        while True:
            print("Known books:", len(self.knownBooks))
            print("\n".join([book.title for book in self.knownBooks]))
            title = input("Type the full title of your book:\n")
            for book in self.knownBooks:
                if title == book.title:
                    print("You chose ", title)
                    self.bookItems.append(BookItem(book))
                    return book

            add = input(
                "Book with title " + title + " not found. Do you want to add them? (y/n) ") == "y"
            if add:
                book = self.add_book()
                self.bookItems.append(BookItem(book))
                print("Added!")
                return book
            print("Try again.")

    def select_author(self):
        while True:
            authors = {book.author for book in self.knownBooks}
            print("Available authors:", len(authors))
            print("\n".join([author.getFullName() for author in authors]))
            name = input("Type the full name of your author:\n")

            for author in authors:
                if name == author.getFullName():
                    print("You chose", name)
                    return author

            add = input(
                "Author with name " + name + " not found. Do you want to add them? (y/n) ") == "y"
            if add:
                author = Author(input("Give a number for the author: \n"), name.split(" ")[0],
                                " ".join(name.split(" ")[1:]))
                print("You chose", author.getFullName())
                return author
            print("Try again.")

    def show_known_books(self):
        print("Known books:", len(self.knownBooks))
        for book in self.knownBooks:
            print(book.isbn, book.title)

    def show_available_books(self):
        print("Available books:", len(self.bookItems))
        for book in self.knownBooks:
            bookItems = [bookItem for bookItem in self.bookItems if bookItem.book.isbn == book.isbn]
            print("items available for book", book.isbn, book.title, ":", len(bookItems))

    def search_books(self):
        print("Sorry, doesn't work yet!")


class Command:
    def __init__(self, commandName, onCommand):
        self.commandName = commandName
        self.onCommand = onCommand


if __name__ == '__main__':
    library = Library()
    print("Welcome to the HR Library system.")


    def do_command(options):
        while True:
            print("These are your options: back, " +
                  ', '.join([c.commandName for c in options]))
            command = input("type in your choice: \n")
            found = False
            for c in options:
                if command == "back":
                    return
                if c.commandName == command:
                    c.onCommand()
                    input("Press enter to continue.\n")
                    found = True
                    break
            if not found:
                print("Invalid option. Try again.")


    def backup():
        global library
        commands = [
            Command("restore", library.restore_from_backup),
            Command("create", library.create_backup),
        ]
        print("You chose backup. What do you want to do now?")
        do_command(commands)


    def notdone():
        print("Sorry, this command is'nt finished yet!")


    def customer():
        commands = [
            Command("add", notdone),
            Command("add_from_csv", notdone),
        ]
        print("You chose customer. What do you want to do now?")
        do_command(commands)


    commands = [
        Command("catalog", library.catalog.enter),
        Command("customer", customer),
        Command("backup", backup),
    ]
    print("What do you want to do?")
    do_command(commands)
