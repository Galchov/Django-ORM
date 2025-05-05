import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from django.db.models import QuerySet
from main_app.models import Author, Book, Review


def find_books_by_genre_and_language(book_genre: str, book_language: str) -> QuerySet:
    books = Book.objects.filter(genre=book_genre, language=book_language)
    return books


def find_authors_nationalities() -> str:
    # Preferred practice
    authors = Author.objects.filter(nationality__isnull=False) 

    # Another way with the same result
    # authors = Author.objects.exclude(nationality=None)

    result = [f"{a.first_name} {a.last_name} is {a.nationality}" for a in authors]
    return '\n'.join(result)


def order_books_by_year() -> str:
    books = Book.objects.order_by('publication_year', 'title')
    result = [f"{b.publication_year} year: {str(b)}" for b in books]
    return '\n'.join(result)


def delete_review_by_id(review_id: int) -> str:
    review = Review.objects.get(pk=review_id)
    review.delete()
    return f"Review by {review.reviewer_name} was deleted"


def filter_authors_by_nationalities(nationality: str) -> str:
    authors = Author.objects.filter(nationality=nationality).order_by('first_name', 'last_name')
    result = [f"{str(a)}" if a.biography is None else f"{a.biography}" for a in authors]
    return '\n'.join(result)


def filter_authors_by_birth_year(first_year: int, second_year: int) -> str:
    authors = Author.objects.filter(birth_date__year__range=(first_year, second_year)).order_by('-birth_date')
    result = [f"{a.birth_date}: {str(a)}" for a in authors]
    return '\n'.join(result)


def change_reviewer_name(current_name: str, new_name: str) -> QuerySet:
    Review.objects.filter(reviewer_name=current_name).update(reviewer_name=new_name)
    result = Review.objects.all()
    return result
