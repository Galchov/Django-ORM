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
)


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
