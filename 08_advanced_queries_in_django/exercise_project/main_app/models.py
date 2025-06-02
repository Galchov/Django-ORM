from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from main_app.managers import RealEstateListingManager, VideoGameManager


class RealEstateListing(models.Model):
    class PropertyTypeChoices(models.TextChoices):
        HOUSE = 'House', 'House',
        FLAT = 'Flat', 'Flat',
        VILLA = 'Villa', 'Villa',
        COTTAGE = 'Cottage', 'Cottage',
        STUDIO = 'Studio', 'Studio',

    property_type = models.CharField(max_length=100, choices=PropertyTypeChoices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    location = models.CharField(max_length=100)

    objects = RealEstateListingManager()


class VideoGame(models.Model):
    class GenreChoices(models.TextChoices):
        ACTION = 'Action', 'Action',
        RPG = 'RPG', 'RPG',
        ADVENTURE = 'Adventure', 'Adventure',
        SPORTS = 'Sports', 'Sports',
        STRATEGY = 'Strategy', 'Strategy',

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GenreChoices)
    release_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1990, message="The release year must be between 1990 and 2023"),
            MaxValueValidator(2023, message="The release year must be between 1990 and 2023"),
        ]
    )
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0, message="The rating must be between 0.0 and 10.0"),
            MaxValueValidator(10.0, message="The rating must be between 0.0 and 10.0"),
        ]
    )

    objects = VideoGameManager()

    def __str__(self):
        return self.title


class BillingInfo(models.Model):
    address = models.CharField(max_length=200)


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    billing_info = models.OneToOneField(BillingInfo, on_delete=models.CASCADE)


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.ManyToManyField(Technology, related_name='projects')


class Programmer(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project, related_name='programmers')


class Task(models.Model):
    class PriorityChoices(models.TextChoices):
        LOW = 'Low', 'Low',
        MEDIUM = 'Medium', 'Medium',
        HIGH = 'High', 'High'

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PriorityChoices)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateField()
    completion_date = models.DateField()


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    difficulty_level = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()
