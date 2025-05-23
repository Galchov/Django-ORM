from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


# Multi-Table Inheritance

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age


class Mammal(Animal):
    fur_color = models.CharField(max_length=50)


class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)


class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


# Abstract Base Classes

# Custom Field Implementation
class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        # Define the choices
        choices = (
            (True, 'Available'),
            (False, 'Not Available'),
        )

        # Set choices and default if not already specified
        kwargs.setdefault('choices', choices)
        kwargs.setdefault('default', True)

        super().__init__(*args, **kwargs)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


class ZooKeeper(Employee):
    class SpecialtyChoices(models.TextChoices):
        MAMMALS = 'Mammals', 'Mammals'
        BIRDS = 'Birds', 'Birds'
        REPTILES = 'Reptiles', 'Reptiles'
        OTHERS = 'Others', 'Others'

    specialty = models.CharField(
        max_length=10,
        choices=SpecialtyChoices,
    )
    managed_animals = models.ManyToManyField(Animal)

    def clean(self):
        super().clean()

        choices = [choice[0] for choice in self.SpecialtyChoices.choices]
        if self.specialty not in choices:
            raise ValidationError("Specialty must be a valid choice.")


class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()


# Proxy Models

class ZooDisplayAnimal(Animal):
    ENDANGERED = ["Cross River Gorilla", "Orangutan", "Green Turtle"]

    class Meta:
        proxy = True

    def display_info(self):
        return f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. It makes a noise like '{self.sound}'."

    def is_endangered(self):
        danger = self.species in self.ENDANGERED
        return f"{self.species} is at risk!" if danger else f"{self.species} is not at risk."

    