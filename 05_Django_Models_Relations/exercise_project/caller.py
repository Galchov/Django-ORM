from datetime import date, timedelta
import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from django.db.models import QuerySet
from main_app.models import Author, Book, Song, Artist, Product, Review, Driver, DrivingLicense, Owner, Car, Registration


# Exercise 1: Library

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


# Exercise 2: Music App

def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    artist = Artist.objects.get(name=artist_name)
    songs = artist.songs.all().order_by('-pk')
    return songs


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


# Exercise 3: Shop

def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    product = Product.objects.get(name=product_name)
    product_reviews = product.reviews.all()

    # Basic:
    # total_rating = 0
    # for review in product_reviews:
    #     review_rating = review.rating
    #     total_rating += review_rating

    # return total_rating / product_reviews.count()

    # Pythonic:
    average_rating = sum(r.rating for r in product_reviews) / len(product_reviews)

    return average_rating


def get_reviews_with_high_ratings(threshold: int) -> QuerySet[Review]:
    # Basic:
    # products = Product.objects.all()
    # high_ratings_reviews = []

    # for product in products:
    #     reviews = product.reviews.all()
    #     for review in reviews:
    #         if review.rating >= threshold:
    #             high_ratings_reviews.append(review)

    # Pythonic:
    high_ratings_reviews = Review.objects.filter(rating__gte=threshold)
    
    return high_ratings_reviews


def get_products_with_no_reviews() -> QuerySet:
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews() -> None:
    Product.objects.filter(reviews__isnull=True).delete()


# Exercise 4: License

def calculate_licenses_expiration_dates() -> str:
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    return '\n'.join(str(l) for l in licenses)


def get_drivers_with_expired_licenses(due_date: date) -> QuerySet[Driver]:
    latest_issue_date = due_date - timedelta(days=365)
    return Driver.objects.filter(license__issue_date__lt=latest_issue_date)


# Exercise 5: Car Registration

def register_car_by_owner(owner: Owner) -> str:
    unapplied_registration = Registration.objects.filter(car__isnull=True).first()
    unregistered_car = Car.objects.filter(registration__isnull=True).first()
    
    unregistered_car.registration = unapplied_registration
    unregistered_car.owner = owner
    unregistered_car.save()

    unapplied_registration.registration_date = date.today()
    unapplied_registration.save()

    return f"Successfully registered {unregistered_car.model} to {str(owner)} with registration number {unapplied_registration.registration_number}."
