import json, csv


class Library:
    id = 0

    @staticmethod
    def generate_id():
        Library.id += 1
        return Library.id

    def __init__(self):
        self.librarians = []
        self.catalog = Catalog()
        self.loan_administration = LoanAdministration()

        self.catalog.load_books()
        self.loan_administration.load_customers()

    def restore_from_backup(self):
        # Todo
        print("Sorry, not done yet!")

    def create_backup(self):
        json.dump(self, open('backup.json', 'w'), default=lambda o: o.__dict__)


class Catalog:
    def __init__(self):
        self.book_items = []
        self.books = []

    def load_books(self):
        jsonbooklist = json.load(open(r'booksset1.json', encoding='UTF-8'))
        for x in jsonbooklist:
            name = x["author"]
            author = Author(name.split(" ")[0], " ".join(name.split(" ")[1:]))
            book = Book(x['title'], [author])

            del x["title"]
            del x["author"]

            book_item = BookItem(book, **x)

            self.books.append(book)
            self.book_items.append(book_item)

    def add_book(self, title, authors):
        book = Book(
            title,
            authors
        )
        self.books.append(book)
        return book

    def add_book_item(self, book):
        book_item = BookItem(book)
        self.book_items.append(book_item)
        return book_item

    def search_books(self, title):
        available_book_items = []
        for item in self.book_items:
            if title in item.book.title and library.loan_administration.check_available(item):
                available_book_items.append(item)
        return available_book_items


class LoanAdministration:
    def __init__(self):
        self.loaned_items = []
        self.customers = []

    def add_customer(self, first_name, last_name, **kwargs):
        customer = Customer(first_name, last_name, **kwargs)
        self.customers.append(customer)
        return customer

    def load_customers(self):
        csv_reader = csv.reader(open(r"FakeNameSet20.csv", encoding='UTF-8'))
        top_row = next(csv_reader)
        for line in csv_reader:
            kwargs = {top_row[i]: line[i] for i in range(0, len(top_row))
                      if top_row[i] not in ["Number", "GivenName", "Surname"]}
            self.add_customer(
                line[top_row.index("GivenName")],
                line[top_row.index("Surname")],
                **kwargs
            )

    def check_available(self, book_item):
        for item in self.loaned_items:
            if item.book_item.id == book_item.id:
                return False
        return True

    def loan_book(self, customer, book_item):
        if not self.check_available(book_item):
            return False

        loan_item = LoanItem(book_item, customer)
        self.loaned_items.append(loan_item)
        return True


class Person:
    def __init__(self, first_name, last_name, **kwargs):
        self.id = Library.generate_id()
        self.first_name = first_name
        self.last_name = last_name
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Customer(Person):
    def __init__(self, first_name, last_name, **kwargs):
        super().__init__(first_name, last_name, **kwargs)


class Librarian(Person):
    def __init__(self, first_name, last_name, **kwargs):
        super().__init__(first_name, last_name, **kwargs)


class Author(Person):
    def __init__(self, first_name, last_name, **kwargs):
        super().__init__(first_name, last_name, **kwargs)


class Book:
    def __init__(self, title, authors):
        self.id = Library.generate_id()
        self.title = title
        self.authors = authors


class BookItem:
    def __init__(self, book, **kwargs):
        self.id = Library.generate_id()
        self.book = book
        for key in kwargs:
            setattr(self, key, kwargs[key])


class LoanItem:
    def __init__(self, book_item, customer):
        self.id = Library.generate_id()
        self.book_item = book_item
        self.customer = customer


if __name__ == '__main__':
    library = Library()

    print("\n-------------––------------")
    print("Make a customer load a book")
    customer = library.loan_administration.customers[0]
    book_item = library.catalog.book_items[5]
    print("customer:", customer.get_full_name(), "book item:", book_item.book.title)
    if library.loan_administration.loan_book(customer, book_item):
        print("loaned: yes")
    else:
        print("loaned:no")
    print("Try again, same items. Should not be able to loan anymore")
    if library.loan_administration.loan_book(customer, book_item):
        print("loaned: yes")
    else:
        print("Failed successfully")

    print("\n-------------––------------")
    print("Search for an available book called The Stranger")
    results = library.catalog.search_books("The Stranger")
    print("Found books:")
    print("\n".join(item.book.title for item in results))

    # todo: make sure works
    print("\n-------------––------------")
    print("Creating a backup")
    library.create_backup()
    print("backup created")
    print("Loan items count:", len(library.loan_administration.loaned_items))
    library = Library()
    print("Reset library")
    print("Loan items count:", len(library.loan_administration.loaned_items))
    library.restore_from_backup()
    print("Restored backup")
    print("Loan items count:", len(library.loan_administration.loaned_items))

    print("\n-------------––------------")
    print("Adding a book:")
    print("Known books count:", len(library.catalog.books))
    print("Add book with title 'A Clash of Kings' and author 'George Martin`")
    book = library.catalog.add_book("A Clash of Kings", [Author("George", "Martin")])
    print("Known books count:", len(library.catalog.books))

    print("\n-------------––------------")
    print("adding a book item:")
    print("Book item count:", len(library.catalog.book_items))
    print("Add book item from the newly created Clash of Kings book`")
    book_item = library.catalog.add_book_item(book)
    print("Book item count:", len(library.catalog.book_items))

    print("\n-------------––------------")
    print("Adding a customer:")
    print("Customer count:", len(library.loan_administration.customers))
    print("Add customer `David Hasselhof`")
    customer = library.loan_administration.add_customer("David", "Hasselhof")
    print("Customer count:", len(library.loan_administration.customers))

    print("\n-------------––------------")
    print("Checking availability of the newly created Clash of Kings book item:")
    print("available:", library.loan_administration.check_available(book_item))
    print("Make David Hasselhof loan it.")
    library.loan_administration.loan_book(customer, book_item)
    print("available:", library.loan_administration.check_available(book_item))
