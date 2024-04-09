# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alcohol(models.Model):
    idalcohol = models.IntegerField(db_column='idAlcohol', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=10, blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alcohol'


class Category(models.Model):
    idcategory = models.IntegerField(db_column='idCategory', primary_key=True)  # Field name made lowercase. The composite primary key (idCategory, Post_idPost) found, that is not supported. The first column is selected.
    category = models.CharField(max_length=8, blank=True, null=True)
    post_idpost = models.ForeignKey('Post', models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'category'
        unique_together = (('idcategory', 'post_idpost'),)


class Cocktail(models.Model):
    idcocktail = models.BigIntegerField(db_column='idCocktail', primary_key=True)  # Field name made lowercase. The composite primary key (idCocktail, Post_idPost) found, that is not supported. The first column is selected.
    name = models.CharField(max_length=45, blank=True, null=True)
    post_idpost = models.ForeignKey('Post', models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cocktail'
        unique_together = (('idcocktail', 'post_idpost'),)


class CocktailHasAlcohol(models.Model):
    cocktail_idcocktail = models.OneToOneField(Cocktail, models.DO_NOTHING, db_column='Cocktail_idCocktail', primary_key=True)  # Field name made lowercase. The composite primary key (Cocktail_idCocktail, Alcohol_idAlcohol) found, that is not supported. The first column is selected.
    alcohol_idalcohol = models.ForeignKey(Alcohol, models.DO_NOTHING, db_column='Alcohol_idAlcohol')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cocktail_has_alcohol'
        unique_together = (('cocktail_idcocktail', 'alcohol_idalcohol'),)


class CocktailHasIngredient(models.Model):
    cocktail_idcocktail = models.OneToOneField(Cocktail, models.DO_NOTHING, db_column='Cocktail_idCocktail', primary_key=True)  # Field name made lowercase. The composite primary key (Cocktail_idCocktail, Ingredient_idIngredient) found, that is not supported. The first column is selected.
    ingredient_idingredient = models.ForeignKey('Ingredient', models.DO_NOTHING, db_column='Ingredient_idIngredient')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cocktail_has_ingredient'
        unique_together = (('cocktail_idcocktail', 'ingredient_idingredient'),)


class Ingredient(models.Model):
    idingredient = models.IntegerField(db_column='idIngredient', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=10, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingredient'


class IngredientHasStore(models.Model):
    ingredient_idingredient = models.OneToOneField(Ingredient, models.DO_NOTHING, db_column='Ingredient_idIngredient', primary_key=True)  # Field name made lowercase. The composite primary key (Ingredient_idIngredient, Store_idStore) found, that is not supported. The first column is selected.
    store_idstore = models.ForeignKey('Store', models.DO_NOTHING, db_column='Store_idStore')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ingredient_has_store'
        unique_together = (('ingredient_idingredient', 'store_idstore'),)


class Keep(models.Model):
    idkeep = models.BigIntegerField(db_column='idKeep', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'keep'


class Keyword(models.Model):
    idkeyword = models.IntegerField(db_column='idKeyword', primary_key=True)  # Field name made lowercase.
    word = models.CharField(max_length=10, blank=True, null=True)
    post_idpost = models.ForeignKey('Post', models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'keyword'


class Like(models.Model):
    idlike = models.BigIntegerField(db_column='idLike', primary_key=True)  # Field name made lowercase. The composite primary key (idLike, Post_idPost) found, that is not supported. The first column is selected.
    accumulate = models.BigIntegerField(blank=True, null=True)
    weekly = models.IntegerField(blank=True, null=True)
    week = models.DateField(blank=True, null=True)
    post_idpost = models.ForeignKey('Post', models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'like'
        unique_together = (('idlike', 'post_idpost'),)
        db_table_comment = '\t\t'


class MakingImages(models.Model):
    idmaking_images = models.BigIntegerField(db_column='idMaking_Images', primary_key=True)  # Field name made lowercase. The composite primary key (idMaking_Images, Post_idPost) found, that is not supported. The first column is selected.
    image_path = models.CharField(max_length=255, blank=True, null=True)
    post_idpost = models.ForeignKey('Post', models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'making_images'
        unique_together = (('idmaking_images', 'post_idpost'),)


class MakingVideo(models.Model):
    idmaking_video = models.BigIntegerField(db_column='idMaking_video', primary_key=True)  # Field name made lowercase.
    video_path = models.CharField(max_length=255, blank=True, null=True)
    post_idpost = models.ForeignKey('Post', models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'making_video'


class Member(models.Model):
    idmember = models.BigAutoField(db_column='idMember', primary_key=True)  # Field name made lowercase.
    email = models.CharField(max_length=30, blank=True, null=True)
    pwd = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    qual = models.IntegerField(blank=True, null=True)
    introduce = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member'


class Post(models.Model):
    idpost = models.BigIntegerField(db_column='idPost', primary_key=True)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    view = models.IntegerField(blank=True, null=True)
    member_idmember = models.ForeignKey(Member, models.DO_NOTHING, db_column='Member_idMember')  # Field name made lowercase.
    keep_idkeep = models.ForeignKey(Keep, models.DO_NOTHING, db_column='Keep_idKeep')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'post'


class Review(models.Model):
    idreview = models.IntegerField(db_column='idReview', primary_key=True)  # Field name made lowercase.
    word = models.CharField(max_length=10, blank=True, null=True)
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'review'


class Season(models.Model):
    idseason = models.IntegerField(db_column='idSeason', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=7, blank=True, null=True)
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'season'


class Store(models.Model):
    idstore = models.IntegerField(db_column='idStore', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store'


class StoreHasAlcohol(models.Model):
    store_idstore = models.OneToOneField(Store, models.DO_NOTHING, db_column='Store_idStore', primary_key=True)  # Field name made lowercase. The composite primary key (Store_idStore, Alcohol_idAlcohol) found, that is not supported. The first column is selected.
    alcohol_idalcohol = models.ForeignKey(Alcohol, models.DO_NOTHING, db_column='Alcohol_idAlcohol')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'store_has_alcohol'
        unique_together = (('store_idstore', 'alcohol_idalcohol'),)


class Times(models.Model):
    idtimes = models.IntegerField(db_column='idTimes', primary_key=True)  # Field name made lowercase.
    when = models.CharField(max_length=5, blank=True, null=True)
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'times'


class Wheather(models.Model):
    idwheather = models.IntegerField(db_column='idWheather', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=10, blank=True, null=True)
    post_idpost = models.ForeignKey(Post, models.DO_NOTHING, db_column='Post_idPost')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wheather'
