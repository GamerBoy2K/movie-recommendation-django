from django.db import models

# Create your models here.

#movie
class movies(models.Model):
    movieId=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=250)
    genres=models.CharField(max_length=250)
    imagePoster = models.ImageField(upload_to='images')  
    class Meta:
        db_table="movies"