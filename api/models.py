from django.db import models

class Company(models.Model):
    username = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    bio = models.TextField()

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.username

class Advocate(models.Model):
    username = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    bio = models.TextField()
    location = models.CharField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField()
    profile_pic_url = models.URLField()
    following_count = models.IntegerField()
    followers_count = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
