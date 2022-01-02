from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.
class Spell(models.Model):
    orig_text = models.CharField(max_length=500)
    spelled_text = models.CharField(max_length=550)
    user = models.ForeignKey(User,
                             on_delete=CASCADE)
    spelled_date = models.DateTimeField(auto_now_add=True)