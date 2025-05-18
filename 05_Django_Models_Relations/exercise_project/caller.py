import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from django.db.models import QuerySet
from main_app.models import Author, Book, Song, Artist, Product, Review


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


def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str) -> QuerySet:
    artist = Artist.objects.get(name=artist_name)
    songs = artist.songs.all().order_by('-pk')
    return songs


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    product = Product.objects.get(name=product_name)
    product_reviews = product.reviews.all()

    total_rating = 0
    for review in product_reviews:
        review_rating = review.rating
        total_rating += review_rating

    return total_rating / product_reviews.count()


def get_reviews_with_high_ratings(threshold: int) -> QuerySet:
    products = Product.objects.all()
    high_ratings_reviews = []

    for product in products:
        reviews = product.reviews.all()
        for review in reviews:
            if review.rating >= threshold:
                high_ratings_reviews.append(review)
    
    return high_ratings_reviews

# TODO: Continue with the Shop functions
