from django.db import models

# Create your models here.


class Enrollment(models.Model):
    FullName = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=12)
    Gender = models.CharField(max_length=20)
    Address = models.TextField()
    DOB = models.CharField(max_length=20)
    SelectMembershipPlan = models.CharField(max_length=20)
    TimeStamp = models.DateTimeField(auto_now_add=True, blank= True)
    def __str__(self):
        return self.FullName


class MembershipPlan(models.Model):
    objects = models.Manager()
    plan = models.CharField(max_length=190)
    price = models.CharField(max_length=50)
    def __int__(self):
        return self.id


