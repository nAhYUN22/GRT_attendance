from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Create your models here.

class SingleUser(AbstractBaseUser, PermissionsMixin):
    ID          = models.CharField(max_length=100, unique=True)
    
    USERNAME_FIELD  = "ID"
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'User'
        
    def save(self, *args, **kwargs):
        # 데이터베이스에 이미 사용자가 존재하면 새 사용자 생성 방지
        if not self.pk and SingleUser.objects.exists():
            raise Exception("Cannot create more than one user.")
        super(SingleUser, self).save(*args, **kwargs)
        
class Student(models.Model):
    name        = models.CharField(max_length=100)
    email       = models.CharField(max_length=100)
    phone_num   = models.CharField(max_length=15)
    
    class Meta:
        db_table = 'Student'
    
