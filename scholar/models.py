from django.db import models

# Create your models here.


class PaperIndex(models.Model):
    serial_no = models.IntegerField(default=0)
    journal_name = models.CharField(max_length=400, primary_key=True)
    scopus = models.CharField(max_length=100, null=True)
    wos = models.CharField(max_length=100, null=True)
    abdc = models.CharField(max_length=100, null=True)
    abs = models.CharField(max_length=100, null=True)
    ft50 = models.CharField(max_length=100, null=True)


class User(models.Model):
    name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)
    otp = models.CharField(max_length=6, blank=True)
    is_verified = models.BooleanField(default=False)
