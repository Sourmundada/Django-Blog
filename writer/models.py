from django.db import models
from django.contrib.auth.models import User

class Writer(User):
    full_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, default='A writer on SM-Blog')
    image = models.ImageField(upload_to='writer-profile/images/', blank=True)

    def __str__(self):
        return self.full_name