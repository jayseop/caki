from django.db import models

# Member 모델
class Member(models.Model):
    idMember = models.AutoField(primary_key=True)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    nickname = models.CharField(max_length=45)
    date = models.DateTimeField(auto_now_add=True)
    qual = models.CharField(max_length=45, default='0')
    introduce = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Member'

# Post 모델
class Post(models.Model):
    idPost=models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    view = models.CharField(max_length=45, default='0')
    text = models.TextField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Post'

# Keep 모델
class Keep(models.Model):
    idKeep=models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Keep'

# Image 모델
class Image(models.Model):
    idImage=models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=100)
    image_path = models.CharField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Image'

# Video 모델
class Video(models.Model):
    idVideo=models.AutoField(primary_key=True)
    video_name = models.CharField(max_length=100)
    video_path = models.CharField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Video'

# Like 모델
class Like(models.Model):
    idLike=models.AutoField(primary_key=True)
    count = models.BigIntegerField(default=0)
    week_count = models.BigIntegerField(default=0)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Like'

# Cocktail 모델
class Cocktail(models.Model):
    title = models.CharField(max_length=100)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Cocktail'

# Ingredient 모델
class Ingredient(models.Model):
    idCocktail=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.BigIntegerField(null=True)
    alcohol = models.BooleanField()
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Ingredient'

# Theme 모델
class Theme(models.Model):
    idTheme=models.AutoField(primary_key=True)
    state = models.CharField(max_length=45)
    tag = models.CharField(max_length=45)

    class Meta:
        db_table = 'Theme'

# Temp 모델
class Temp(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Temp'