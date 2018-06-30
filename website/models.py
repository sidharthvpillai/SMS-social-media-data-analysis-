# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Query(models.Model):
    is_public = models.BooleanField()
    query = models.CharField(max_length=500)
    is_active = models.BooleanField()
    name = models.CharField(max_length=100)

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    validity = models.DateField(null=True, blank=True,)
    transaction_id=models.CharField(max_length=64,null=True)


class FbQueryMapper(models.Model):
    page = models.CharField (max_length=200)

class SocialData(models.Model):
    user_name = models.CharField(max_length=20, default='facebook')
    fbquerymapper = models.ForeignKey(FbQueryMapper,on_delete=models.CASCADE)
    message = models.CharField(max_length=5000)
    created_date = models.DateTimeField()
    sentiment = models.CharField(max_length=20)
    source = models.CharField(max_length=10)
    location = models.CharField(max_length=10)
    like_count = models.IntegerField()
    love_count = models.IntegerField()
    haha_count = models.IntegerField()
    sad_count = models.IntegerField()
    wow_count = models.IntegerField()
    angry_count = models.IntegerField()
    thankful_count = models.IntegerField()
    shares= models.IntegerField()
    link = models.URLField(max_length=200 , unique= True)
    def __str__(self):
        return "%s..." % self.message[:15]

class SocialDataQuery(models.Model):
   class Meta:
       unique_together=[("socialdata","query")]
   socialdata = models.ForeignKey(SocialData,on_delete=models.CASCADE)
   query = models.ForeignKey(Query, on_delete=models.CASCADE)


#SELECT * FROM website_socialdata WHERE message @@ to_tsquery('happy | happy&birthday');
#SELECT  * FROM website_socialdata, to_tsquery('neutrino|(dark & matter)') query WHERE query @@ message