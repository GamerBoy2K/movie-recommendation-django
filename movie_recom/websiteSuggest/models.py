from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#movie
class movies(models.Model):
    movieId=models.AutoField(primary_key=True)
    title=models.CharField(max_length=250)
    genres=models.CharField(max_length=250)
    imagePoster = models.ImageField(upload_to='images',default='images/nonPoster.png')  
    class Meta:
        db_table="movies"

class watchLater(models.Model):
    userId=models.ForeignKey(User,on_delete=models.CASCADE)
    movieNum=models.ForeignKey(movies,on_delete=models.CASCADE)
    class Meta:
        db_table="watchLater"