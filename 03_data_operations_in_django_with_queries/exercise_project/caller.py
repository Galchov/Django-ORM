import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
from django.db.models import F


# ===== Task 1 =====
def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(
        name=name,
        species=species,
    )

    return f"{pet.name} is a very cute {pet.species}!"


# ===== Task 2 =====
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
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()


# ===== Task 3 =====
def show_all_locations() -> str:
    all_locations = Location.objects.all().order_by('-id')
    locations_sorted = []
    for l in all_locations:
        locations_sorted.append(f"{l.name} has a population of {l.population}!")
    
    return '\n'.join(locations_sorted)


def new_capital() -> None:
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals():
    capitals = Location.objects.filter(is_capital=True).values('name')

    return capitals


def delete_first_location() -> None:
    first_location = Location.objects.first()
    first_location.delete()


# ===== Task 4 =====
def apply_discount() -> None:
    all_cars = Car.objects.all()
    for car in all_cars:
        number = car.year
        discount_percentage = 0
        while number > 0:
            discount_percentage += number % 10
            number //= 10
        
        new_price = car.price - (car.price * discount_percentage / 100)
        car.price_with_discount = new_price
        car.save()


def get_recent_cars() -> list:
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car() -> None:
    Car.objects.last().delete()


# ===== Task 5 =====
def show_unfinished_tasks() -> str:
    unfinished_tasks = Task.objects.filter(is_finished=False)
    return '\n'.join(f"Task - {t.title} needs to be done until {t.due_date}!" for t in unfinished_tasks)


def complete_odd_tasks() -> None:
    all_tasks = Task.objects.all()
    for t in all_tasks:
        if t.pk % 2 == 1:
            t.is_finished = True
        t.save()


def encode_and_replace(text: str, task_title: str) -> None:
    all_tasks = Task.objects.all()
    encoded_text = ""
    for sym in text:
        new_symbol = chr(ord(sym) - 3)
        encoded_text += new_symbol
    
    for task in all_tasks:
        if task.title == task_title:
            task.description = encoded_text
        task.save()


# ===== Task 6 =====
def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(room_type=HotelRoom.RoomTypes.DELUXE)
    deluxe_rooms_even_id = [room for room in deluxe_rooms if room.pk % 2 == 0]

    return "\n".join(
        f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!" 
        for r in deluxe_rooms_even_id
        )


def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.filter(is_reserved=True).order_by('id')
    previous_room: HotelRoom = None

    for room in rooms:
        if previous_room:
            room.capacity += previous_room.capacity
        else:
            room.capacity += room.pk

        previous_room = room
        room.save()


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()
    if not last_room.is_reserved:
        last_room.delete()


# ===== Task 7 =====
def update_characters() -> None:
    # Preferred method:
    Character.objects.filter(class_name=Character.ClassNameChoices.MAGE).update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7,
    )

    Character.objects.filter(class_name=Character.ClassNameChoices.WARRIOR).update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4,
    )

    Character.objects.filter(class_name__in=[Character.ClassNameChoices.ASSASSIN, Character.ClassNameChoices.SCOUT]).update(
        inventory="The inventory is empty"
    )

    # Not preferred method:
    # characters = Character.objects.all()
    # for c in characters:
    #     if c.class_name == "Mage":
    #         c.level += 3
    #         c.intelligence -= 7
    #     elif c.class_name == "Warrior":
    #         c.hit_points /= 2
    #         c.dexterity += 4
    #     elif c.class_name in ("Assasin", "Scout"):
    #         c.inventory = "The inventory is empty"
    #     c.save()


def fuse_characters(first_character: Character, second_character: Character) -> None:
    new_name = f"{first_character.name} {second_character.name}"
    new_class_name = Character.ClassNameChoices.FUSION
    new_level = (first_character.level + second_character.level) // 2
    new_strength = (first_character.strength + second_character.strength) * 1.2
    new_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    new_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    new_hit_points = first_character.hit_points + second_character.hit_points
    new_inventory = None

    if first_character.class_name in [Character.ClassNameChoices.MAGE, Character.ClassNameChoices.SCOUT]:
        new_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in (Character.ClassNameChoices.ASSASSIN, Character.ClassNameChoices.WARRIOR):
        new_inventory = "Dragon Scale Armor, Excalibur"

    mega_character = Character.objects.create(
        name=new_name,
        class_name=new_class_name,
        level=new_level,
        strength=new_strength,
        dexterity=new_dexterity,
        intelligence=new_intelligence,
        hit_points=new_hit_points,
        inventory=new_inventory,
    )

    first_character.delete()
    second_character.delete()


def grant_dexterity() -> None:
    Character.objects.update(dexterity=30)


def grant_intelligence() -> None:
    Character.objects.update(intelligence=40)


def grant_strength() -> None:
    Character.objects.update(strength=50)


def delete_characters() -> None:
    Character.objects.filter(inventory="The inventory is empty").delete()


# ===== Tests =====

# Task 1:
# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

# Task 2:
# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)

# Task 3:
# def create_locations() -> None:
#     Location.objects.create(
#         name="Sofia",
#         region="Sofia Region",
#         population=1329000,
#         description="The capital of Bulgaria and the largest city in the country",
#         is_capital=False,
#     )

#     Location.objects.create(
#         name="Plovdiv",
#         region="Plovdiv Region",
#         population=346942,
#         description="The second-largest city in Bulgaria with a rich historical heritage",
#         is_capital=False,
#     )

#     Location.objects.create(
#         name="Varna",
#         region="Varna Region",
#         population=330486,
#         description="A city known for its sea breeze and beautiful beaches on the Black Sea",
#         is_capital=False,
#     )

#     return "Locations added successfully."
#
# print(create_locations())
# print(show_all_locations())
# print(new_capital())
# print(get_capitals())

# Task 4:
# def insert_cars() -> None:
#     Car.objects.create(
#         model="Mercedes C63 AMG",
#         year=2019,
#         color="white",
#         price=120000.00,
#     )
#     Car.objects.create(
#         model="Audi Q7 S line",
#         year=2023,
#         color="black",
#         price=183900.00,
#     )
#     Car.objects.create(
#         model="Chevrolet Corvette",
#         year=2021,
#         color="dark grey",
#         price=199999.00,
#     )
#     return "Car added to the Database."
#
# print(insert_cars())
# apply_discount()
# print(get_recent_cars())

# Task 5:
# def create_task() -> None:
#     Task.objects.create(
#         title="Sample Task",
#         description="This is a sample task description",
#         due_date="2023-10-31",
#         is_finished=False,
#     )
#     return "Task added successfully."
#
# print(create_task())
# encode_and_replace("Zdvk#wkh#glvkhv$", "Sample Task")
# print(Task.objects.get(title='Sample Task').description)

# Task 6:
# def insert_rooms() -> None:
#     HotelRoom.objects.create(
#         room_number=401,
#         room_type="Standard",
#         capacity=2,
#         amenities="Tv",
#         price_per_night=100.00,
#     )
#     HotelRoom.objects.create(
#         room_number=501,
#         room_type="Deluxe",
#         capacity=3,
#         amenities="Wi-Fi",
#         price_per_night=200.00,
#     )
#     HotelRoom.objects.create(
#         room_number=601,
#         room_type="Deluxe",
#         capacity=6,
#         amenities="Jacuzzi",
#         price_per_night=400.00,
#     )
#     return "Rooms created successfully."
#
# print(insert_rooms())
# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)

# Task 7:
# print(create_characters())
# update_characters()

# character1 = Character.objects.create(
#         name='Gandalf',
#         class_name='Mage',
#         level=10,
#         strength=15,
#         dexterity=20,
#         intelligence=25,
#         hit_points=100,
#         inventory='Staff of Magic, Spellbook',
#     )
# character2 = Character.objects.create(
#     name='Hector',
#     class_name='Warrior',
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory='Sword of Troy, Shield of Protection',
# )

# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()

# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)
