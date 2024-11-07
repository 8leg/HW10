from pydoc_data.topics import topics


class Book:

    def __init__(self, title, author, isbn, year_published):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year_published = year_published


class FictionBook(Book):

    def __init__(self, title, author, isbn, year_published, genres):
        super().__init__(title, author, isbn, year_published)
        self.genres = genres

    def get_info(self):
        return {'title': self.title, 'author': self.author, 'isbn': self.isbn, 'year_published': self.year_published,
                'genres': self.genres}



class NonFictionBook(Book):

    def __init__(self, title, author, isbn, year_published, topics):
        super().__init__(title, author, isbn, year_published)
        self.topics = topics

    def get_info(self):
        return {'title': self.title, 'author': self.author, 'isbn': self.isbn, 'year_published': self.year_published,
                'topics': self.topics}


class ReferenceBook(Book):

    def __init__(self, title, author, isbn, year_published, description):
        super().__init__(title, author, isbn, year_published)
        self.description = description

    def get_info(self):
        return {'title': self.title, 'author': self.author, 'isbn': self.isbn, 'year_published': self.year_published,
                'description': self.description}


class Library:

    def __init__(self):
        self.__books = []

    def add_book(self, title, author, isbn, year_published, book_type, genres=None, topics=None, description=None):
        if book_type=='fiction':
            if type(genres)==str:
                genres=genres.split(',')
            elif type(genres)!=list:
                raise ValueError('genres must be a list or str separated by comma')
            self.__books.append(FictionBook(title, author, isbn, year_published, genres))

        elif book_type=='nonfiction':
            if type(topics)==str:
                topics=topics.split(',')
            elif type(topics)!=list:
                raise ValueError('genres must be a list or str separated by comma')
            self.__books.append(NonFictionBook(title, author, isbn, year_published, topics))

        elif book_type=='reference':
            if type(description)!=str:
                raise ValueError('description must be a string')
            self.__books.append(ReferenceBook(title, author, isbn, year_published, description))

    def remove_book(self, value, criteria='auto'):
        removed=0
        if criteria=='auto':
            for book in self.__books:
                this_book = book.get_info()
                for i in this_book.values():
                    if value in i and type(i)==list:
                        self.__books.remove(book)
                        removed+=1
                    elif value==i:
                        self.__books.remove(book)
                        removed+=1

        else:
            for book in self.__books:
                this_book = book.get_info()
                if criteria in this_book.keys():
                    if value in this_book[criteria]:
                        self.__books.remove(book)
                        removed+=1
        return removed

    def get_books(self):
        for book in self.__books:
            yield book.get_info()

    def get_books_by_category(self, category):
        for i in self.get_books():
            for j in i.keys():
                if category in i[j]:
                    yield i
                elif category==i[j]:
                    yield i

    def get_books_by_author(self, author):
        for i in self.get_books():
            if i['author'] == author:
                yield i

    def get_books_by_year(self, published_year):
        for i in self.get_books():
            if i['year_published'] == published_year:
                yield i

if __name__ == '__main__':
    lib = Library()
    try:
        lib.add_book('451 degrees fahrenheit', 'Ray Bradbury', '156', '1953',
                     'fiction','Novel,Science fiction,Dystopian Fiction,Political fiction')
        lib.add_book('1984', 'George Orwell', '823', '1949', 'fiction',
                     'Science fiction,Dystopian Fiction,Social science fiction,Political fiction')
        lib.add_book('the code book', 'Simon Lehna Singh', '978', '1999',
                     'nonfiction', topics='codebreaking')
        lib.add_book('Mistborn: The Final Empire', 'Brandon Sanderson', '4533', '2006',
                     'fiction', genres='High fantasy')
    except ValueError:
        print('Something went wrong')
    for i in lib.get_books_by_year(1999):
        print(i)
    for i in lib.get_books_by_author('Brandon Sanderson'):
        print(i)
    lib.remove_book('451')
    for i in lib.get_books_by_category('Science fiction'):
        print(i)