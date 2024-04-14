from django.db import models

# Member 모델
class Member(models.Model):
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    nickname = models.CharField(max_length=45)
    date = models.DateTimeField(auto_now_add=True)
    qual = models.CharField(max_length=45, default='0')
    introduce = models.CharField(max_length=100, blank=True, null=True)

# Post 모델
class Post(models.Model):
    title = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    view = models.CharField(max_length=45, default='0')
    text = models.TextField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

# Keep 모델
class Keep(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

# Image 모델
class Image(models.Model):
    image_name = models.CharField(max_length=100)
    image_path = models.CharField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

# Video 모델
class Video(models.Model):
    video_name = models.CharField(max_length=100)
    video_path = models.CharField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

# Like 모델
class Like(models.Model):
    count = models.BigIntegerField(default=0)
    week_count = models.BigIntegerField(default=0)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

# Cocktail 모델
class Cocktail(models.Model):
    title = models.CharField(max_length=100)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

# Ingredient 모델
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    price = models.BigIntegerField(null=True)
    alcohol = models.BooleanField()
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)

# Theme 모델
class Theme(models.Model):
    state = models.CharField(max_length=45)
    tag = models.CharField(max_length=45)

# Temp 모델
class Temp(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)