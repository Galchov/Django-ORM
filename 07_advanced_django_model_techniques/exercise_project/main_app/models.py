from django.db import models
from django.core.validators import MinValueValidator
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
