from django.db import models


class Categories(models.Model):
    yelp_name = models.CharField(max_length=200)
    human_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.human_name


class YelpCredentials(models.Model):
    user_id = models.CharField(max_length=200)
    consumer_key = models.CharField(max_length=200)
    consumer_secret = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
    token_secret = models.CharField(max_length=200)

    def __unicode__(self):
        return (self.user_id, self.consumer_key)


class GoogleMapsCredentials(models.Model):
    user_id = models.IntegerField()
    api_key = models.CharField(max_length=200)

    def __unicode__(self):
        return self.api_key
