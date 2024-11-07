import os
from typing import List

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import (
    ChessPlayer,
    Meal,
    Dungeon,
    Workout,
    ArtworkGallery,
    Laptop,
)


# ----- Exercise 1 -----
def show_highest_rated_art() -> str:
    top_rated_art = ArtworkGallery.objects.order_by('-rating', 'id').first()

    return (f"{top_rated_art.art_name} is the highest-rated art "
            f"with a {top_rated_art.rating} rating!")


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts() -> None:
    ArtworkGallery.objects.filter(rating__lt=0).delete()


# ----- Exercise 2 -----
def show_the_most_expensive_laptop() -> str:
    most_expensive = Laptop.objects.order_by('-price', '-id').first()

    return (f"{most_expensive.brand} is the most expensive laptop "
            f"available for {most_expensive.price}$!")


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)


def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(memory=16)


# TODO: Plenty of exercises are remaining. Will be continued soon.
