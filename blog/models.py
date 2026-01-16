from django.db import models
from django.contrib.auth.models import User
import os


class Journey(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    song = models.FileField(upload_to='journey_songs/', blank=True, null=True)

    def __str__(self):
        return self.title


class JourneyImage(models.Model):
    journey = models.ForeignKey(Journey, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='journey_images/')

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


class Comment(models.Model):
    journey = models.ForeignKey(Journey, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    journey = models.ForeignKey(Journey, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('journey', 'user')
