from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Posts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="post")
    image = models.ImageField(upload_to="posts/media/uploads/",blank=True,null=True)
    title = models.CharField(max_length=200)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date =models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ['upload_date',]

class Like(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="like_post")
    user  = models.ForeignKey(User,on_delete=models.CASCADE,related_name="liker")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}  {self.post}"

