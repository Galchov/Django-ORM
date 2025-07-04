from django.core.exceptions import ValidationError


def validate_menu_categories(value):
    required_categories = ["Appetizers", "Main Course", "Desserts"]
    missing = [category for category in required_categories if category not in value]
    if missing:
        raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')
        