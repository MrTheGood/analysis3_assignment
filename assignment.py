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
        print("todo: restore backup")

    def create_backup(self):
        print("todo: create backup")


class LoanAdministration:
    def __init__(self):
        self.loanedItems = []


class Catalog:
    def __init__(self):
        self.bookItems = []
        self.knownBooks = []


class Command:
    def __init__(self, commandName, onCommand):
        self.commandName = commandName
        self.onCommand = onCommand


if __name__ == '__main__':
    library = Library()
    print("Welcome to the HR Library system.")


    def do_command(options):
        while True:
            command = input("type in your choice: \n")
            for c in options:
                if c.commandName == command:
                    c.onCommand()
                    return
            print("Invalid option. Try again.")


    enabled = True
    while enabled:
        def quit():
            global enabled
            enabled = False


        def backup():
            global library
            commands = [
                Command("restore", library.restore_from_backup),
                Command("create", library.create_backup),
            ]
            print("You chose backup. What do you want to do now?\n" +
                  ', '.join([c.commandName for c in commands]))
            do_command(commands)


        def book():
            commands = [
                Command("loan", None),
                Command("return", None),
                Command("search", None),
                Command("add", None),
            ]
            print("You chose book. What do you want to do now?\n" +
                  ', '.join([c.commandName for c in commands]))
            do_command(commands)


        def customer():
            commands = [
                Command("add", None),
                Command("add_from_csv", None),
            ]
            print("You chose customer. What do you want to do now?\n" +
                  ', '.join([c.commandName for c in commands]))
            do_command(commands)


        commands = [
            Command("quit", quit),
            Command("book", book),
            Command("customer", customer),
            Command("backup", backup),
        ]
        print("What do you want to do? You have the following options: \n" +
              ', '.join([c.commandName for c in commands]))
        do_command(commands)
