from django.db import models

def min_length(value):
	if len(value) < 10:
		raise ValidationError('Entered field must be ' +
								'longer than 10 characters.')

# Create your models here.
class Profile(models.Model):
	firstname = models.CharField(max_length=25)
	lastname = models.CharField(max_length=25)
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField()
	password = models.CharField(max_length=25)
	birthdate = models.DateField()
	bio = models.TextField(validators=[min_length])
	avatar = models.BooleanField(blank=True)
	
	
	def __str__(self):
		return self.firstname
		
