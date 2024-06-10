from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="account")
    image = models.ImageField(upload_to="accounts/media/uploads/",blank=True,null=True)
    description =models.TextField(blank=True,null=True)
    date_of_birth= models.DateField(blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    facebook = models.URLField(blank=True,null=True)
    linkedin = models.URLField(blank=True,null=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
    
    def is_followed_by(self, user):
        return Follow.objects.filter(follower=user, following=self.user).exists()
    



class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    time = models.DateTimeField(auto_now_add=True)



