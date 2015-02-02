from django.db import models
from django.contrib.auth.modles import User


class Categories(models.Model):
    yelp_name = models.CharField(max_length=200)
    human_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.human_name


class YelpCredentials(models.Model):
    user = models.OneToOneField(User)
    consumer_key = models.CharField(max_length=100)
    consumer_secret = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    token_secret = models.CharField(max_length=100)

    def __unicode__(self):
        return (self.user_id, self.consumer_key)

