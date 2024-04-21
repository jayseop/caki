# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework import serializers

class UserManager(BaseUserManager):
    def create_user(self, email, password, nickname, qual, introduce,**kwargs):

        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
            nickname = nickname,
            qual = qual,
            introduce = introduce 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


# AbstractBaseUser를 상속해서 유저 커스텀
# Member 모델

class Member(AbstractBaseUser):
    idmember = models.BigAutoField(db_column='idMember', primary_key=True)  # Field name made lowercase.
    email = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=130)
    nickname = models.CharField(unique=True, max_length=45)
    date = models.DateTimeField(auto_now_add=True)
    qual = models.CharField(max_length=4, blank=True, null=True)
    introduce = models.CharField(max_length=255, blank=True, null=True)
    
    last_login = None

    USERNAME_FIELD = 'email'
    objects = UserManager()
    class Meta:
        db_table = 'Member'


class Post(models.Model):
    idpost = models.BigAutoField(db_column='idPost', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=300)
    date = models.DateTimeField()
    view = models.CharField(max_length=45)
    text = models.CharField(max_length=8000)
    member_idmember = models.ForeignKey(Member, models.DO_NOTHING, db_column='Member_idMember')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'post'

class Cocktail(models.Model):
    idcocktail = models.BigAutoField(db_column='idCocktail', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=100)
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cocktail'


class Image(models.Model):
    idimage = models.BigAutoField(db_column='idImage', primary_key=True)  # Field name made lowercase.
    image_name = models.CharField(max_length=100)
    image_path = models.CharField(max_length=300)
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'image'


class Ingredient(models.Model):
    idingredient = models.BigAutoField(db_column='idIngredient', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100)
    price = models.BigIntegerField(blank=True, null=True)
    alcohol = models.IntegerField()
    cocktail_idcocktail = models.ForeignKey(Cocktail, models.DO_NOTHING, db_column='Cocktail_idCocktail')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'ingredient'


class Keep(models.Model):
    idkeep = models.BigAutoField(db_column='idKeep', primary_key=True)  # Field name made lowercase.
    member_idmember = models.ForeignKey(Member, models.DO_NOTHING, db_column='Member_idMember')  # Field name made lowercase.
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'keep'


class Like(models.Model):
    idlike = models.BigAutoField(db_column='idLike', primary_key=True)  # Field name made lowercase.
    count = models.BigIntegerField()
    week_count = models.BigIntegerField()
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'like'


class Theme(models.Model):
    idtheme = models.BigAutoField(db_column='idTheme', primary_key=True)  # Field name made lowercase.
    state = models.CharField(max_length=45)
    tag = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'theme'


class Temp(models.Model):
    theme_idtheme = models.OneToOneField(Theme, models.DO_NOTHING, db_column='Theme_idTheme', primary_key=True)  # Field name made lowercase. The composite primary key (Theme_idTheme, Post_idPost) found, that is not supported. The first column is selected.
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'temp'
        unique_together = (('theme_idtheme', 'post_idpost'),)


class Video(models.Model):
    idvideo = models.BigAutoField(db_column='idVideo', primary_key=True)  # Field name made lowercase.
    video_name = models.CharField(max_length=100)
    video_path = models.CharField(max_length=300)
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'video'
