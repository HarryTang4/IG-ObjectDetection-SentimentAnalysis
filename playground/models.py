from django.db import models

# Create your models here.


class Register(models.Model):
    firstname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)


class Login(models.Model):
    firstname = models.CharField(max_length=100)
    username = models.ForeignKey(
        Register, blank=True, null=True, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)


class User(models.Model):
    firstname = models.CharField(max_length=100)
    username = models.ForeignKey(
        Register, blank=True, null=True, on_delete=models.CASCADE)


class Photos(models.Model):
    img1 = models.ImageField(null=True, blank=True, upload_to='photos/')
    img2 = models.ImageField(null=True, blank=True, upload_to='photos/')
    img3 = models.ImageField(null=True, blank=True, upload_to='photos/')
    img4 = models.ImageField(null=True, blank=True, upload_to='photos/')
    img5 = models.ImageField(null=True, blank=True, upload_to='photos/')
    img6 = models.ImageField(null=True, blank=True, upload_to='photos/')

    def __str__(self):
        return self.img1
