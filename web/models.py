from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
 
class Input_data(models.Model):
    name = models.CharField(max_length=100,default='SOME STRING')
    List = models.TextField()
    newicks=models.TextField()
    
    
class Panel(models.Model):
    name = models.CharField(max_length=100,default='SOME STRING')
    selected= models.CharField(max_length=50,default="select")
   
    
class Matrix(models.Model):
    metric = models.CharField(max_length=100,default='SOME STRING')
    Grid = ArrayField(ArrayField(models.FloatField()))

    
class Tree_model(models.Model):
    name = models.CharField(max_length=100,default='trees_details')
    Tree1 = models.IntegerField(default=1)
    Tree2=  models.IntegerField(default=2)
    Metric= models.CharField(max_length=50,default="select")   
    
    

    
    