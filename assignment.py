class Person:
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

    def getFullName(self):
        return self.firstName + " " + self.lastName


class Costumer(Person):
    def __init__(self, firstName, lastName,gender,nameSet,streetAddress,zipCode,city,emailAddress,userName,telephoneNumber):
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.nameSet = nameSet
        self.streetAddress = streetAddress
        self.zipCode = zipCode
        self.city = city
        self.emailAddress = emailAddress
        self.userName = userName
        self.telephoneNumber = telephoneNumber
        super().__init__(firstName, lastName, gender, nameSet, streetAddress, zipCode, city, emailAddress, userName, telephoneNumber)


class Libarian(Person):
    def __init__(self, firstName, lastName):
        super().__init__(firstName, lastName)


class Author(Person):
    def __init__(self, firstName, lastName):
        super().__init__(firstName, lastName)


class Book:
    def __init__(self, Author, isbn, country, link, pages, title, year, imagelink, language):
        self.Author = Author
        self.isbn = isbn
        self.country = country
        self.link = link
        self.pages = pages
        self.title = title
        self.year = year
        self.imagelink = imagelink
        self.language = language


class BookItem(Book):
    def __init__(self, Author, isbn, country, link, pages, title, year, imagelink, language):
        super().__init__(Author, isbn, country, link, pages, title, year, imagelink, language)


class LoanItem(BookItem):

    def __init__(self, Author, isbn, country, link, pages, title, year, imagelink, language):
        super().__init__(Author, isbn, country, link, pages, title, year, imagelink, language)


class Library:
    def __init__(self):
        self.customers = ()
        self.librarians = ()
        self.catalog = Catalog()
        self.loanAdministration = LoanAdministration()


class LoanAdministration:
    def __init__(self):
        pass


class Catalog:
    def __init__(self):
        pass
