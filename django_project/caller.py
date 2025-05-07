import os
import django
from typing import List
from django.db.models import Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon


##### ArtworkGallery #####

def show_highest_rated_art() -> str:
    arts = ArtworkGallery.objects.order_by('-rating', 'pk')
    highest_rated = arts.first()
    return f"{highest_rated.art_name} is the highest-rated art with a {highest_rated.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts() -> None:
    ArtworkGallery.objects.filter(rating__lt=0).delete()


##### Laptop #####

def show_the_most_expensive_laptop() -> str:
    laptops = Laptop.objects.filter('-price', '-pk')
    most_expensive = laptops.first()
    return f"{most_expensive.brand} is the most expensive laptop available for {most_expensive.price}$!"


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=[
        Laptop.BrandChoices.ASUS,
        Laptop.BrandChoices.LENOVO,
    ]).update(storage=512)


def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=[
        Laptop.BrandChoices.APPLE,
        Laptop.BrandChoices.DELL,
        Laptop.BrandChoices.ACER,
    ]).update(memory=16)


def update_operation_systems() -> None:
    Laptop.objects.update(
        operation_system=Case(
            When(brand=Laptop.BrandChoices.ASUS, then=Value(Laptop.OperationSystemChoices.WINDOWS)),
            When(brand=Laptop.BrandChoices.APPLE, then=Value(Laptop.OperationSystemChoices.MACOS)),
            When(brand=Laptop.BrandChoices.LENOVO, then=Value(Laptop.OperationSystemChoices.CHROME_OS)),
            When(brand__in=[
                Laptop.BrandChoices.DELL,
                Laptop.BrandChoices.ACER,
            ], then=Value(Laptop.OperationSystemChoices.LINUX)),
        )
    )


def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()


##### ChessPlayer #####

def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players() -> None:
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won() -> None:
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost() -> None:
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn() -> None:
    ChessPlayer.objects.all().update(games_drawn=10)


def grant_chess_title_GM() -> None:
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


def grant_chess_title_IM() -> None:
    ChessPlayer.objects.filter(rating__range=(2300, 2399)).update(title='IM')


def grant_chess_title_FM() -> None:
    ChessPlayer.objects.filter(rating__range=(2200, 2299)).update(title='FM')


def grant_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__range=(0, 2199)).update(title='regular player')


##### Meal #####

def set_new_chefs() -> None:
    Meal.objects.update(
        chef=Case(
            When(meal_type=Meal.MealTypeChoices.BREAKFAST, then=Value('Gordon Ramsay')),
            When(meal_type=Meal.MealTypeChoices.LUNCH, then=Value('Julia Child')),
            When(meal_type=Meal.MealTypeChoices.DINNER, then=Value('Jamie Oliver')),
            When(meal_type=Meal.MealTypeChoices.SNACK, then=Value('Thomas Keller')),
        )
    )
    

def set_new_preparation_times() -> None:
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type=Meal.MealTypeChoices.BREAKFAST, then=Value('10 minutes')),
            When(meal_type=Meal.MealTypeChoices.LUNCH, then=Value('12 minutes')),
            When(meal_type=Meal.MealTypeChoices.DINNER, then=Value('15 minutes')),
            When(meal_type=Meal.MealTypeChoices.SNACK, then=Value('5 minutes')),
        )
    )


def update_low_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=[
        Meal.MealTypeChoices.BREAKFAST,
        Meal.MealTypeChoices.DINNER,
    ]).update(calories=400)


def update_high_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=[
        Meal.MealTypeChoices.LUNCH,
        Meal.MealTypeChoices.SNACK,
    ]).update(calories=700)


def delete_lunch_and_snack_meals() -> None:
    Meal.objects.filter(meal_type__in=[
        Meal.MealTypeChoices.LUNCH,
        Meal.MealTypeChoices.SNACK,
    ]).delete()


##### Dungeon #####

def show_hard_dungeons() -> str:
    hard_dungeons = Dungeon.objects.filter(difficulty=Dungeon.DifficultyChoices.HARD)
    return '\n'.join(f"{d.name} is guarded by {d.boss_name} who has {d.boss_health} health points!"
                      for d in hard_dungeons)


def bulk_create_dungeons(args: List[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)


def update_dungeon_names() -> None:
    Dungeon.objects.update(
        name=Case(
            When(difficulty=Dungeon.DifficultyChoices.EASY, then=Value('The Erased Thombs')),
            When(difficulty=Dungeon.DifficultyChoices.MEDIUM, then=Value('The Coral Labyrinth')),
            When(difficulty=Dungeon.DifficultyChoices.HARD, then=Value('The Lost Haunt')),
        )
    )


def update_dungeon_bosses_health() -> None:
    Dungeon.objects.exclude(difficulty=Dungeon.DifficultyChoices.EASY).update(boss_health=500)


def update_dungeon_recommended_levels() -> None:
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty=Dungeon.DifficultyChoices.EASY, then=Value(25)),
            When(difficulty=Dungeon.DifficultyChoices.MEDIUM, then=Value(50)),
            When(difficulty=Dungeon.DifficultyChoices.HARD, then=Value(75)),
        )
    )


def update_dungeon_rewards() -> None:
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then=Value('1000 Gold')),
            When(location__startswith='E', then=Value('New dungeon unlocked')),
            When(location__endswith='s', then=Value('Dragonheart Amulet')),
        )
    )


def set_new_locations() -> None:
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss')),
        )
    )
