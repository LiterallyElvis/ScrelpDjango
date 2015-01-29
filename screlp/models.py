from django.db import models


class Categories(models.Model):
    yelp_name = models.CharField(max_length=200)
    human_name = models.CharField(max_length=200)


class YelpCredentials(models.Model):
    consumer_key = models.CharField(max_length=200)
    consumer_secret = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
    token_secret = models.CharField(max_length=200)


class GoogleMapsCredentials(models.Model):
    api_key = models.CharField(max_length=200)
