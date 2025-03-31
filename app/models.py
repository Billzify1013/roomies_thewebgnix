from django.contrib.auth.models import User
from django.db import models
import uuid
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

class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Hotel(BaseModel):
    """
    Represents a hotel, storing details such as name, description, pricing, availability,
    and customer ratings.
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255)
    landmark = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    badge = models.CharField(max_length=255,blank=True,null=True)
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    hotel_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='hotels')
    hotel_main_img = models.ImageField(upload_to='hotel_main_image')
    hotel_contact_number = models.IntegerField(default=0)
    is_verify = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)

    @property
    def remaining_price(self):
        """Calculates the difference between the original and offer price."""
        if self.offer_price:
            return self.price_per_night - self.offer_price
        return 0  # No discount applied
    
    def __str__(self):
        return self.name


class Hotel_image_category(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    image_category_name = models.CharField(max_length=250,null=None,blank=True)


class Hotel_all_images(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    img_category = models.ForeignKey(Hotel_image_category,on_delete=models.CASCADE)
    hotel_img = models.ImageField(upload_to='hotel_all_image')


class hotel_aminities(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    aminities_name = models.CharField(max_length=250,null=None,blank=True)
    icon_code = models.CharField(max_length=250,null=None,blank=True)


class hotel_more_details(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    hotel_owner_name = models.CharField(max_length=250,default=None)
    hotel_contact = models.IntegerField(default=0)
    hotel_state = models.CharField(max_length=50,default=None)
    hotel_city = models.CharField(max_length=50,default=None)
    hotel_zipcode =  models.CharField(max_length=20,default=None)
    hotel_address = models.CharField(max_length=250,default=None)
    hotel_gstnumber = models.CharField(max_length=20,blank=True,null=True)


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


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} - {self.hotel.name}"
    

class Room_category(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=300,null=True,blank=True)
    cat_description = models.TextField(null=True,blank=True)
    category_code = models.CharField(max_length=300,null=True,blank=True)
    category_badge = models.CharField(max_length=50,null=True,blank=True)
    is_active = models.BooleanField(default=True)


class room_category_image(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    category = models.ForeignKey(Room_category,on_delete=models.CASCADE)
    hotel_img = models.ImageField(upload_to='category_image')


class Influencer(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='influencer_profile')
    profile_picture = models.ImageField(upload_to='influencer_profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='city_influencers')
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name='hotel_influencers')
    bio = models.TextField(blank=True, null=True)
    followers_count = models.PositiveIntegerField(default=0)
    social_media_links = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.user.username
    