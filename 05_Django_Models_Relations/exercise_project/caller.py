import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Author, Book


def show_all_authors_with_their_books() -> str:
    authors = Author.objects.all().order_by('pk')
    authors_with_books = []

    for author in authors:
        author_books = author.books.all()

        if not author_books:
            continue

        books_titles = ', '.join(book.title for book in author_books)
        authors_with_books.append(f"{author.name} has written - {books_titles}!")
    
    return '\n'.join(authors_with_books)


def delete_all_authors_without_books() -> None:
    Author.objects.filter(books__isnull=True).delete()
