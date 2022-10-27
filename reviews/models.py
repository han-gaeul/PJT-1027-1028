from distutils.command.upload import upload
from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, Thumbnail

# Create your models here.

class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(
        upload_to = 'images/',
        blank=True,
        processors=[ResizeToFill(500, 500)],
        format='JPEG',
        options={'quality': 100},
    )
    thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(300, 300)],
        format='JPEG',
        options={'quality' : 100},
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    like_users = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='like_reviews')

class Comments(models.Model):
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)