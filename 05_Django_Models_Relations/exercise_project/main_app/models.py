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
