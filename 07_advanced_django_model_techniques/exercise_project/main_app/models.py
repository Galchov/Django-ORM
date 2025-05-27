from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
from main_app.custom_validators import NameValidator, PhoneNumberValidator


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[NameValidator("Name can only contain letters and spaces")],
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18, message="Age must be greater than or equal to 18")],
    )
    email = models.EmailField(
        error_messages={"invalid": "Enter a valid email address"}
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[PhoneNumberValidator("Phone number must start with '+359' followed by 9 digits")],
    )
    website_url = models.URLField(
        error_messages={"invalid": "Enter a valid URL"}
    )


class BaseMedia(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']


class Book(BaseMedia):
    author = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(5, message="Author must be at least 5 characters long"),
        ]
    )
    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(6, message="ISBN must be at least 6 characters long"),
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"


class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(8, message="Director must be at least 8 characters long"),
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"


class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(9, message="Artist must be at least 9 characters long"),
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"
