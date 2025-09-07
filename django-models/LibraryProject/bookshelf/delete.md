from bookshelf.models import Book

>>> book = Book.objects.all()[0]

>>> book

<Book: Book object (1)>
>>> book.title

'1984'

>>> book.delete

<bound method Model.delete of <Book: Book object (1)>>

>>> book = Book.objects.all()[0]

>>> Book.objects.all()

<QuerySet [<Book: Book object (1)>]>