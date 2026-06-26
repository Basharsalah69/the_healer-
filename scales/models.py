from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField( max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    

class Assements(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    score_phq9 =models.IntegerField(default=0)
    score_gad7 =models.IntegerField(default=0)
    complete_at=models.DateTimeField(auto_now_add=True)
    
