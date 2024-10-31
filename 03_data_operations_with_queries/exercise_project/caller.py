import os
import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import (
    Pet,
    Artifact,
    Location,
    Car,
    Task,
    HotelRoom,
)


# Assistance functions:
def get_discount_percent(year: int) -> int:
    percent = 0
    for digit in str(year):
        percent += int(digit)

    return percent


# CRUD functions:
def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(
        name=name,
        species=species,
    )

    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str) -> None:
    # Artifact.objects.filter(is_magical=True, age__gt=250, pk=artifact.pk).update(name=new_name)
    # UPDATE artifact SET name = new_name WHERE is_magical=TRUE && age > 250 && id = 1

    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    # all_artifacts = Artifact.objects.all()
    # all_artifacts.delete()

    Artifact.objects.all().delete()


def show_all_locations() -> str:
    # First attempt without string dunder method in the model:

    # all_locations = Location.objects.all()
    #
    # locations_list = list(all_locations)
    # new_list = sorted(locations_list, key=lambda x: x.id, reverse=True)
    #
    # return '\n'.join(f"{l.name} has a population of {l.population}!" for l in new_list)

    # Optimized solution (The model now has a dunder method):
    locations = Location.objects.all().order_by('-id')

    return '\n'.join(str(l) for l in locations)


def new_capital() -> None:
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals() -> QuerySet:
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location() -> None:
    Location.objects.first().delete()


def apply_discount() -> None:
    cars = Car.objects.all()

    for car in cars:
        discount_percent = get_discount_percent(car.year)
        total_discount = discount_percent / 100 * float(car.price)
        car.price_with_discount = float(car.price) - total_discount
        car.save()


def get_recent_cars() -> QuerySet:
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car() -> None:
    Car.objects.last().delete()


def show_unfinished_tasks() -> str:
    unfinished_tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(str(t) for t in unfinished_tasks)


def complete_odd_tasks() -> None:
    # for task in Task.objects.all():
    #     if task.id % 2 == 1:
    #         task.is_finished = True
    #         task.save()

    # Using 'bulk_update' method:
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 == 1:
            task.is_finished = True

    Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str) -> None:
    # tasks = Task.objects.filter(title=task_title)
    #
    # new_description = ''
    # for symbol in text:
    #     new_symbol = ord(symbol) - 3
    #     new_description += chr(new_symbol)
    #
    # for task in tasks:
    #     task.description = new_description
    #     task.save()

    # Optimized solution:
    decoded_text = ''.join(chr(ord(symbol) - 3) for symbol in text)
    Task.objects.filter(title=task_title).update(description=decoded_text)


def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(room_type="Deluxe")
    even_deluxe_rooms = [str(r) for r in deluxe_rooms if r.id % 2 == 0]

    return "\n".join(even_deluxe_rooms)


def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.all().order_by('id')

    previous_room_capacity = None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity is not None:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room() -> None:
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room() -> None:
    room = HotelRoom.objects.last()

    if not room.is_reserved:
        room.delete()


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


# print(create_artifact("Ancient Sword",
#                       "Lost Kingdom",
#                       500,
#                       "A legendary sword with a rich history",
#                       True))
# print(create_artifact("Crystal Amulet",
#                       "Mystic Forest",
#                       300,
#                       "A magical amulet believed to bring good fortune",
#                       True))
# print(create_artifact("Stone Tablet",
#                       "Ruined Temple",
#                       1000,
#                       "An ancient tablet covered in mysterious inscriptions",
#                       False))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)

# print(show_all_locations())
# print(new_capital())
# print(get_capitals())

# apply_discount()
# print(get_recent_cars())

# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title='Simple Task').description)

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)
