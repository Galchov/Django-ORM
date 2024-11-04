import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review


def find_books_by_genre_and_language(book_genre: str, book_language: str) -> str:
    books = Book.objects.filter(genre=book_genre, language=book_language)
    return books


def find_authors_nationalities() -> str:
    result = []
    authors = Author.objects.exclude(nationality__isnull=True)
    # Author.objects.exclude(nationality=None)

    for a in authors:
        result.append(f'{a.first_name} {a.last_name} is {a.nationality}')

    return '\n'.join(result)


def order_books_by_year() -> str:
    result = []
    books = Book.objects.order_by('publication_year', 'title')

    for b in books:
        result.append(f'{b.publication_year} year: {b.title} by {b.author}')

    return '\n'.join(result)


def delete_review_by_id(review_id: int) -> str:
    review = Review.objects.get(id=review_id)
    review.delete()

    return f'Review by {review.reviewer_name} was deleted'


def filter_authors_by_nationalities(author_nationality: str) -> str:
    authors = Author.objects.filter(nationality=author_nationality).order_by('first_name', 'last_name')
    result = [a.biography
              if a.biography is not None
              else f'{a.first_name} {a.last_name}'
              for a in authors]

    return '\n'.join(result)


# print(find_books_by_genre_and_language("Romance", "English"))
# print(find_books_by_genre_and_language("Poetry", "Spanish"))
# print(find_books_by_genre_and_language("Mystery", "English"))

# print(find_authors_nationalities())

# print(order_books_by_year())

# print(delete_review_by_id(4))
# print(delete_review_by_id(1))
# print(delete_review_by_id(8))

# print("American authors:")
# print(filter_authors_by_nationalities('American'))
# print()
# print("British authors:")
# print(filter_authors_by_nationalities('British'))
# print()
# print("Authors with no nationalities:")
# print(filter_authors_by_nationalities(None))
