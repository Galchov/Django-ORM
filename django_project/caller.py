import os
import django
from typing import List
from django.db.models import F, Q, Case, When, Value, QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import ChessPlayer, Meal, Dungeon, Workout, ArtworkGallery, Laptop


def show_highest_rated_art() -> str:
    arts = ArtworkGallery.objects.order_by('-rating', 'pk')
    best_art = arts.first()
    return f"{best_art.art_name} is the highest-rated art with a {best_art.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts() -> None:
    negative_rated_arts = ArtworkGallery.objects.filter(rating__lt=0)
    negative_rated_arts.delete()


def show_the_most_expensive_laptop() -> str:
    laptops = Laptop.objects.order_by('-price', '-pk')
    most_expensive = laptops.first()
    return f"{most_expensive.brand} is the most expensive laptop available for {most_expensive.price}$!"


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=["Asus", "Lenovo"]).update(storage=512)


def update_to_16_memory() -> None:
    Laptop.objects.filter(brand__in=["Apple", "Dell", "Acer"]).update(memory=16)


def update_operation_systems() -> None:
    Laptop.objects.update(
        operation_system=Case(
            When(brand="Asus", then=Value(Laptop.OSTypeChoices.WINDOWS)),
            When(brand="Apple", then=Value(Laptop.OSTypeChoices.MACOS)),
            When(brand="Lenovo", then=Value(Laptop.OSTypeChoices.CHROMEOS)),
            When(brand__in=["Dell", "Acer"], then=Value(Laptop.OSTypeChoices.LINUX))
        )
    )

    # Laptop.objects.filter(brand=Laptop.BrandTypeChoices.ASUS).update(operation_system=Laptop.OSTypeChoices.WINDOWS)
    # Laptop.objects.filter(brand=Laptop.BrandTypeChoices.APPLE).update(operation_system=Laptop.OSTypeChoices.MACOS)
    # Laptop.objects.filter(brand__in=[Laptop.BrandTypeChoices.DELL, Laptop.BrandTypeChoices.ACER]).update(
    #     operation_system=Laptop.OSTypeChoices.LINUX
    # )
    # Laptop.objects.filter(brand=Laptop.BrandTypeChoices.LENOVO).update(operation_system=Laptop.OSTypeChoices.CHROMEOS)


def delete_inexpensive_laptops() -> None:
    low_cost_laptops = Laptop.objects.filter(price__lt=1200)
    low_cost_laptops.delete()


# ==== Test Code =====
# artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)

# Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())

# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )

# Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]

# Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)

# update_to_512_GB_storage()
# update_operation_systems()

# Retrieve 2 laptops from the database
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()

# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)
