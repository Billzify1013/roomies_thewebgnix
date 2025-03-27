from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class BaseModel(models.Model):
    """
    Abstract base model to provide common fields for all models.
    Includes timestamp fields for auditing and an `is_active` flag for soft deletion.
    """
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set when the record is first created
    updated_at = models.DateTimeField(auto_now=True)  # Auto-update whenever the record is modified
    is_active = models.BooleanField(default=True)  # Soft delete indicator (instead of hard delete)

    class Meta:
        abstract = True  # This ensures Django doesn’t create a separate table for this model


class Hotel(BaseModel):
    """
    Represents a hotel, storing details such as name, description, pricing, availability,
    and customer ratings.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    badge = models.CharField(max_length=255)
    total_rooms = models.PositiveIntegerField()
    available_rooms = models.PositiveIntegerField()
    rating = models.FloatField(default=0)

    @property
    def remaining_price(self):
        """Calculates the difference between the original and offer price."""
        if self.offer_price:
            return self.price_per_night - self.offer_price
        return 0  # No discount applied
    
    def __str__(self):
        return self.name


class Room(BaseModel):
    """
    Represents a room in a hotel, storing details such as room type, pricing,
    capacity, and available amenities.
    """
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    amenities = models.TextField(blank=True)

    def __str__(self):
        return f"{self.room_type} at {self.hotel.name}"


class Address(BaseModel):
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name="address")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    landmarks = models.JSONField(default=list)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.city}, {self.country}"


class HotelImage(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='hotel_images/')
    image_type = models.CharField(
        max_length=50, 
        choices=[('Room', 'Room'), ('Lobby', 'Lobby'), ('Pool', 'Pool'), ('Restaurant', 'Restaurant')],
        default='Room'
    )

    def __str__(self):
        return f"{self.hotel.name} - {self.image_type}"


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} - {self.hotel.name}"
