from django.db.models import Count, Prefetch

from .models import Book, Store
from .query_debugger import query_debugger


@query_debugger
def book_list():
    queryset = Book.objects.all()

    books = []
    for book in queryset:
        books.append({'id': book.id, 'name': book.name, 'publisher': book.publisher.name})

    return books


@query_debugger
def book_list_select_related():

    queryset = Book.objects.select_related('publisher').all()

    books = []

    for book in queryset:
        books.append({'id': book.id, 'name': book.name, 'publisher': book.publisher.name})

    return books


@query_debugger
def store_list():

    queryset = Store.objects.all()

    stores = []

    for store in queryset:
        books = [book.name for book in store.books.all()]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger
def store_list_prefetch_related():
    queryset = Store.objects.prefetch_related('books')

    stores = []

    for store in queryset:
        books = [book.name for book in store.books.all()]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger
def store_list_expensive_books_prefetch_related():
    queryset = Store.objects.prefetch_related('books')

    stores = []
    for store in queryset:
        books = [book.name for book in store.books.filter(price__range=(250, 300))]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger
def store_list_expensive_books_prefetch_related_efficient():

    queryset = Store.objects.prefetch_related(
        Prefetch('books', queryset=Book.objects.filter(price__range=(250, 300))))

    stores = []
    for store in queryset:
        books = [book.name for book in store.books.all()]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger
def stores_per_books():

    stores = Store.objects.annotate(cnt=Count('books'))

    return stores
