from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.conf import settings
import os

#현재 시간

# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, email, password, nickname, qual, introduce, image_path, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
            nickname=nickname,
            qual=qual,
            introduce=introduce,
            image_path=image_path
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

# Function to define upload path for Member images
def member_upload_to(instance, filename):
    nickname_directory = 'profile/' + instance.nickname
    directory = os.path.join('media', nickname_directory)
    os.makedirs(directory, exist_ok=True)
    return os.path.join(nickname_directory, filename)

# Custom user model
class Member(AbstractBaseUser):
    idmember = models.BigAutoField(db_column='idMember', primary_key=True)  # Field name made lowercase.
    email = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=130)
    nickname = models.CharField(unique=True, max_length=45)
    date = models.DateTimeField(default=timezone.localtime(timezone.now())
)
    qual = models.CharField(max_length=4, blank=True)
    introduce = models.CharField(max_length=255, blank=True)
    image_path = models.ImageField(upload_to=member_upload_to, blank=True)

    last_login = None

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        db_table = 'member'

    def delete(self, *args, **kargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image_path.name))
        return super(Member, self).delete(*args, **kargs)

# Function to define upload path for Post images
def post_upload_to(instance, filename):
    post_directory = 'post/' + str(instance.post_idpost)
    directory = os.path.join('media', post_directory)
    os.makedirs(directory, exist_ok=True)
    return os.path.join(post_directory, filename)

# Post model
class Post(models.Model):
    idpost = models.BigAutoField(db_column='idPost', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=300)
    date = models.DateTimeField(default=timezone.localtime(timezone.now())
)
    text = models.CharField(max_length=8000)
    member_idmember = models.ForeignKey(Member, models.CASCADE, db_column='Member_idMember')  # Field name made lowercase.

    class Meta:
        db_table = 'post'

# Cocktail model
class Cocktail(models.Model):
    idcocktail = models.BigAutoField(db_column='idCocktail', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=100)
    post_idpost = models.ForeignKey(Post, models.CASCADE, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        db_table = 'cocktail'

# Image model
class Image(models.Model):
    idimage = models.BigAutoField(db_column='idImage', primary_key=True)  # Field name made lowercase.
    image_name = models.CharField(max_length=100)
    image_path = models.ImageField(upload_to=post_upload_to, blank=True)
    post_idpost = models.ForeignKey(Post, models.CASCADE, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        db_table = 'image'

    def delete(self, *args, **kargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image_path.name))
        return super(Image, self).delete(*args, **kargs)

# Ingredient model
class Ingredient(models.Model):
    idingredient = models.BigAutoField(db_column='idIngredient', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100)
    price = models.BigIntegerField(blank=True)
    alcohol = models.IntegerField()
    cocktail_idcocktail = models.ForeignKey(Cocktail, models.CASCADE, db_column='Cocktail_idCocktail')  # Field name made lowercase.

    class Meta:
        db_table = 'ingredient'

# Keep model
class Keep(models.Model):
    idkeep = models.BigAutoField(db_column='idKeep', primary_key=True)  # Field name made lowercase.
    member_idmember = models.ForeignKey(Member, models.CASCADE, db_column='Member_idMember')  # Field name made lowercase.
    post_idpost = models.ForeignKey(Post, models.CASCADE, db_column='Post_idPost')  # Field name made lowercase.
    date = models.DateTimeField(default=timezone.localtime(timezone.now())
)

    class Meta:
        db_table = 'keep'

class Postviews(models.Model):
    idpostviews = models.BigAutoField(db_column='idPostviews', primary_key=True)  # Field name made lowercase.
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='post_idpost')  # Field name made lowercase.
    member_idmember = models.ForeignKey(Member, models.DO_NOTHING, db_column='Member_idMember')  # Field name made lowercase.
    date = models.DateTimeField(default=timezone.localtime(timezone.now())
)

    class Meta:
        managed = False
        db_table = 'postviews'

# Like model
class Like(models.Model):
    idlike = models.BigAutoField(db_column='idLike', primary_key=True)  # Field name made lowercase.
    post_idpost = models.ForeignKey(Post, models.CASCADE, db_column='Post_idPost')  # Field name made lowercase.
    member_idmember = models.ForeignKey(Member, models.CASCADE, db_column='Member_idMember')  # Field name made lowercase.
    date = models.DateTimeField(default=timezone.localtime(timezone.now())
)
    weather = models.TextField(blank=True)

    class Meta:
        db_table = 'like'

# Review model
class Review(models.Model):
    idreview = models.BigAutoField(db_column='idReview', primary_key=True)  # Field name made lowercase.
    post_idpost = models.ForeignKey(Post, models.CASCADE, db_column='Post_idPost')
    member_idmember = models.ForeignKey(Member, models.CASCADE, db_column='Member_idMember')  # Field name made lowercase.
    review = models.TextField()

    class Meta:
        db_table = 'review'

# Tag model
class Tag(models.Model):
    idtag = models.BigAutoField(db_column='idTag', primary_key=True)  # Field name made lowercase.
    post_idpost = models.OneToOneField(Post, models.CASCADE, db_column='Post_idPost')  # Field name made lowercase.
    tag = models.TextField()

    class Meta:
        db_table = 'tag'

# Video model
class Video(models.Model):
    idvideo = models.BigAutoField(db_column='idVideo', primary_key=True)  # Field name made lowercase.
    video_name = models.CharField(max_length=100)
    video_path = models.CharField(max_length=300)
    post_idpost = models.ForeignKey(Post, models.CASCADE, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        db_table = 'video'
