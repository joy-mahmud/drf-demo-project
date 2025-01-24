from django.db import models

# Create your models here.
class Publisher(models.Model):
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    published_date=models.DateField()
    publisher=models.ForeignKey(Publisher,related_name='books',on_delete=models.CASCADE,null=True)

