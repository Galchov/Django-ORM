import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Pet, Artifact, Location


# Task 1:
def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(
        name=name,
        species=species,
    )

    return f"{pet.name} is a very cute {pet.species}!"


# Task 2:
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


# Task 3:
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
# print(create_locations())
# print(show_all_locations())
# print(new_capital())
# print(get_capitals())
