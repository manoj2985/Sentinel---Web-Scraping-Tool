from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AllWord(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    all_word = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class TotalMatchWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    words = models.CharField(max_length=200, null=True, blank=True)
    count = models.CharField(max_length=100, default=1, null=True, blank=True)

    def __str__(self) -> str:
        return self.words

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    your_url  = models.CharField(max_length=200, null=True, blank=True)
    alldetail = models.TextField(null=True, blank=True, default={})
    total_uword = models.CharField(max_length=200, null=True, blank=True)
    total_word = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username