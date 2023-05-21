from django.db import models

# Create your models here.

#movie
class movies(models.Model):
    movieId=models.AutoField(primary_key=True)
    title=models.CharField(max_length=250)
    genres=models.CharField(max_length=250)
    imagePoster = models.ImageField(upload_to='images',default='images/nonPoster.png')  
    class Meta:
        db_table="movies"