from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
from main_app.custom_validators import NameValidator, PhoneNumberValidator
from main_app.mixins import RechargeEnergyMixin


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


class Product(models.Model):
    TAX_PERCENT: Decimal = Decimal('0.08')
    SHIPPING_MULTIPLIER: Decimal = Decimal('2.00')

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self) -> Decimal:
        return self.price * self.TAX_PERCENT
    
    def calculate_shipping_cost(self, weight: Decimal) -> Decimal:
        return weight * self.SHIPPING_MULTIPLIER
    
    def format_product_name(self) -> str:
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    TAX_PERCENT: Decimal = Decimal('0.05')
    SHIPPING_MULTIPLIER: Decimal = Decimal('1.50')
    PRICE_INCREASE_PERCENT: Decimal = Decimal('0.20')

    class Meta:
        proxy = True

    def calculate_price_without_discount(self) -> float:
        return self.price + (self.price * self.PRICE_INCREASE_PERCENT)
    
    def format_product_name(self):
        return f"Discounted Product: {self.name}"


class Hero(models.Model, RechargeEnergyMixin):
    ENERGY_CONSUMPTION: int = 0
    MIN_ENERGY: int = 1

    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()

    @property
    def required_energy_message(self) -> str:
        return ""
    
    @property
    def success_message(self) -> str:
        return ""

    def use_ability(self):
        if self.energy < self.ENERGY_CONSUMPTION:
            return self.required_energy_message
        
        if self.energy - self.ENERGY_CONSUMPTION > 0:
            self.energy -= self.ENERGY_CONSUMPTION
        else:
            self.energy = self.MIN_ENERGY

        self.save()

        return self.success_message
        

class SpiderHero(Hero):
    ENERGY_CONSUMPTION: int = 80

    class Meta:
        proxy = True
    
    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    @property
    def success_message(self) -> str:
        return f"{self.name} as Spider Hero swings from buildings using web shooters"
    
    def swing_from_buildings(self) -> str:
        return self.use_ability()


class FlashHero(Hero):
    ENERGY_CONSUMPTION: int = 65

    class Meta:
        proxy = True
    
    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    @property
    def success_message(self) -> str:
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"
    
    def run_at_super_speed(self) -> str:
        return self.use_ability()
