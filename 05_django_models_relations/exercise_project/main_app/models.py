import datetime
from django.db import models


# Exercise 1: Library

class Author(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


# Exercise 2: Music App

class Song(models.Model):
    title = models.CharField(max_length=100, unique=True)


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    songs = models.ManyToManyField(Song, related_name='artists')


# Exercise 3: Shop

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    description = models.TextField(max_length=200)
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"{self.rating} => {self.description}"


# Exercise 4: License

class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DrivingLicense(models.Model):
    license_number = models.CharField(max_length=10, unique=True)
    issue_date = models.DateField()
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name='license')

    def __str__(self):
        expiration_date = self.issue_date + datetime.timedelta(days=365)
        return f"License with number: {self.license_number} expires on {expiration_date}!"


# Exercise 5: Car Registration

class Owner(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    owner = models.ForeignKey(
        Owner, 
        on_delete=models.CASCADE, 
        related_name='cars',
        null=True,
        blank=True,
    )


class Registration(models.Model):
    registration_number = models.CharField(max_length=10, unique=True)
    registration_date = models.DateField(null=True, blank=True)
    car = models.OneToOneField(
        Car, 
        on_delete=models.CASCADE, 
        related_name='registration',
        null=True,
        blank=True,
    )
