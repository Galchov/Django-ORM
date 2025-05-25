from datetime import date, timedelta
from enum import StrEnum

from django.db import models
from django.db.models import QuerySet
from django.core.exceptions import ValidationError


class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)


class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)


class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)


class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(max_length=100)



class UserProfile(models.Model):
    username = models.CharField(
        max_length=70,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )
    bio = models.TextField(
        null=True,
        blank=True,
    )


class Message(models.Model):
    sender = models.ForeignKey(
        to=UserProfile,
        related_name='sent_messages',
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        to=UserProfile,
        related_name='received_messages',
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    is_read = models.BooleanField(
        default=False,
    )

    def mark_as_read(self) -> None:
        self.is_read = True
        self.save(update_fields=['is_read'])

    def reply_to_message(self, reply_content: str) -> 'Message':
        new_message = Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content,
        )

        return new_message

    def forward_message(self, receiver: UserProfile) -> 'Message':
        new_message = Message.objects.create(
            sender=self.receiver,
            receiver=receiver,
            content=self.content
        )

        return new_message



class StudentIDField(models.PositiveIntegerField):

    @staticmethod
    def validate_data(value) -> int:
        try:
            return int(float(value))
        except ValueError:
            raise ValueError("Invalid input for student ID")

    # Convert the input value into a proper Python int
    def to_python(self, value) -> int:
        return self.validate_data(value)
    
    # Prepare the field's value before saving it to the Database
    def get_prep_value(self, value) -> int:
        validated_value = self.validate_data(value)

        if validated_value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")
        
        return validated_value


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()



class MaskedCreditCardField(models.CharField):
    description = "Stores and masks a credit card number"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20   # Enforce max_length = 20
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        """Convert the input value to the masked format before saving to DB"""

        value = self.to_python(value)
        return self._mask_card_number(value)
    
    def from_db_value(self, value, expression, connection):
        """Returns already masked string from DB"""

        return value

    def to_python(self, value):
        """Ensure the value is valid and converted to a string"""

        if value is None:
            return value
        
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")
        
        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")
        
        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")
        
        return value
    
    def _mask_card_number(self, number):
        return "****-****-****-" + number[-4:]


class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField(max_length=20)



# ===== Hotel Reservation System =====

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
    )
    number = models.CharField(
        max_length=100,
        unique=True,
    )
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def clean(self) -> None:
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")
        
    def save(self, *args, **kwargs) -> str:
        self.clean()
        super().save(*args, **kwargs)

        return f"Room {self.number} created successfully"


class ReservationTypes(StrEnum):
    REGULAR = "Regular"
    SPECIAL = "Special"


class BaseReservation(models.Model):
    class Meta:
        abstract = True

    reservation_type = None
    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    
    def reservation_period(self) -> int:
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self) -> float:
        total_cost = self.reservation_period() * self.room.price_per_night
        return round(total_cost, 2)
    
    def get_overlapping_reservations(self, start_date: date, end_date: date) -> QuerySet['BaseReservation']:
        return self.__class__.objects.filter(
            room=self.room,
            end_date__gte=start_date,
            start_date__lte=end_date,
        )
    
    @property
    def is_available(self) -> bool:
        reservations = self.get_overlapping_reservations(self.start_date, self.end_date)
        return not reservations.exists()
    
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")
        
        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")
        
    def save(self, *args, **kwargs) -> str:
        self.clean()
        super().save(*args, **kwargs)
        return f"{self.reservation_type} reservation for room {self.room.number}"
    

class RegularReservation(BaseReservation):
    reservation_type = ReservationTypes.REGULAR.value


class SpecialReservation(BaseReservation):
    reservation_type = ReservationTypes.SPECIAL.value

    def extend_reservation(self, days: int) -> str:
        new_end_date = self.end_date + timedelta(days=days)
        reservations = self.get_overlapping_reservations(self.start_date, new_end_date)

        if reservations:
            raise ValidationError("Error during extending reservation")
        
        self.end_date = new_end_date
        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"
