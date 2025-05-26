from django.contrib import admin
from main_app.models import RestaurantReview


@admin.register(RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):
    pass
