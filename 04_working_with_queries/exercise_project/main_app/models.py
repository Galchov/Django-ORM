from django.db import models

from main_app.choices import (
    LaptopBrandChoice,
    OperationSystemChoice
)


class ArtworkGallery(models.Model):
    artist_name = models.CharField(max_length=100)
    art_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Laptop(models.Model):
    brand = models.CharField(max_length=20, choices=LaptopBrandChoice.choices)
    processor = models.CharField(max_length=100)
    memory = models.PositiveIntegerField(help_text="Memory in GB")
    storage = models.PositiveIntegerField(help_text="Storage in GB")
    operation_system = models.CharField(max_length=20, choices=OperationSystemChoice.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
