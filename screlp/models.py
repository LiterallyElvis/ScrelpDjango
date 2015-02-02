from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Categories(models.Model):
    yelp_name = models.CharField(max_length=200)
    human_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.human_name


class ScrelpUser(AbstractBaseUser):
    username = models.EmailField(max_length=200)    

    yelp_consumer_key = models.CharField(max_length=100)
    yelp_consumer_secret = models.CharField(max_length=100)
    yelp_token = models.CharField(max_length=100)
    yelp_token_secret = models.CharField(max_length=100)

    def __unicode__(self):
        return (self.username)

