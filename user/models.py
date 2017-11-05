from django.db import models
#from user.forms import UserRegistrationForm
# Create your models here.


# Create your models here.

class KeyWord(models.Model):
	key=models.CharField(max_length=30,null=True,default='')
class Author(models.Model):
	name=models.CharField(max_length=255,null=False,primary_key=True)
	def __str__(self):
		return self.name
		
class Documents(models.Model):
	
	user_id=models.IntegerField(null=False,default=1)
	title=models.CharField(max_length=255,blank=False)
	abstract=models.TextField(max_length=200,blank=False)
	document=models.FileField(upload_to='document')
	CSE='Computer Science and Engineering'
	ECE='Electronic and Communincation'
	EEE='Electrical and Electronic Engineering'
	ME='Mechanical Engineering'
	CE='Civil Engineering'
	branchs=(
		(CSE,'Computer Science and Engineering'),
		(ECE,'Electronic and Communincation'),
		(EEE,'Electrical and Electronic Engineering'),
		(ME,'Mechanical Engineering'),
		(CE,'Civil Engineering'),
		)
	branch=models.CharField(choices=branchs,default=CSE,max_length=200)
	pr='PRIVATE'
	pu='PUBLIC'
	visible=(
		(pr,'PRIVATE'),
		(pu,'PUBLIC'),
		)
	visibilty=models.CharField(choices=visible,default=pu,max_length=200)
	author=models.ForeignKey(Author,on_delete=models.CASCADE,null=False)
	key=models.ForeignKey(KeyWord,on_delete=models.CASCADE,null=True,default='')
	
	
	def __str__(self):
		return self.title
