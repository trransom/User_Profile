from django.db import models

def min_length(value):
	if len(value) < 10:
		raise ValidationError('Entered field must be ' +
								'longer than 10 characters.')

# Create your models here.
class Profile(models.Model):
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	username = models.CharField(max_length=50)
	email = models.EmailField()
	password = models.CharField(max_length=25)
	birthdate = models.DateField()
	bio = models.TextField(validators=[min_length])
	avatar = models.NullBooleanField(null=True)
	
	
	def __str__(self):
		return self.first_name
		
