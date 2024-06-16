from django.db import models
from django.utils.timezone import now
import os

# Create your models here.
class Listing(models.Model):

    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'
        FOR_RENT = 'For Rent'

    class HomeType(models.TextChoices):
        HOUSE = 'House'
        CONDO = 'Condo'
        TOWNHOUSE = 'Townhouse'

    # as a result separate db, we can not have a Foreign key relations
    realtor = models.EmailField(max_length=255) #links our User model to Listing model
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=20)
    description = models.TextField() # Because they are longer text characters
    bedrooms = models.IntegerField()
    price = models.IntegerField(default=0)
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1) #i.e. max_length..
    # .. example: 3.2 (seeing that it only contains 2 digits)
    sale_type = models.CharField(max_length=10, choices=SaleType.choices, default=SaleType.FOR_SALE)
    home_type = models.CharField(max_length=255, choices=HomeType.choices, default=HomeType.HOUSE) 
    main_photo = models.ImageField(upload_to='listings/')
    photo_1 = models.ImageField(upload_to='listings/')
    photo_2 = models.ImageField(upload_to='listings/')
    photo_3 = models.ImageField(upload_to='listings/')
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)

    def delete(self, *args, **kwargs):
        # print(f"Deleting listing: {self.title}")
        # print(f"Deleting main_photo: {self.main_photo.path}")
        # print(f"Deleting photo_1: {self.photo_1.path}")
        # print(f"Deleting photo_2: {self.photo_2.path}")
        # print(f"Deleting photo_3: {self.photo_3.path}")

        # Deletes the media inside of the file folder
        if os.path.isfile(self.main_photo.path):
            os.remove(self.main_photo.path)
        if os.path.isfile(self.photo_1.path):
            os.remove(self.photo_1.path)
        if os.path.isfile(self.photo_2.path):
            os.remove(self.photo_2.path)
        if os.path.isfile(self.photo_3.path):
            os.remove(self.photo_3.path)
            
        # continues with deleting from db
        super().delete(*args, **kwargs)

    # Provided by AI
    # class Meta:
    #     app_label = 'listing'
    #     db_table = 'listing_listing'  # Optional: Specify custom table name
    #     verbose_name = 'Listing'
    #     verbose_name_plural = 'Listings'

    def __str__(self):
        return self.title
    
    # def __str__(self):
    #     return str(self.id)  # Return UUID as string representation