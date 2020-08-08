from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
class StaffManager(BaseUserManager):
    def create_user(self,email,name,password):
        if not email:
            return ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email,name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,name,password):
        user = self.create_user(email,name,password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
class Staff(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password']
    objects = StaffManager

    def __str__(self):
        return self.mail
    def get_full_name(self):
        return self.name
class Project(models.Model):
    project_name = models.CharField(max_length=255,unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.project_name
class ProjectDocument(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    document_title = models.CharField(max_length=255,unique=True)
    document = models.FileField(upload_to='media/documents/project')
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.document_title
class ProjectTask(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    task_title = models.CharField(max_length=255,unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.task_title
class ProjectBudget(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    budget_item = models.CharField(max_length=255,unique=True)
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=18,decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.budget_item

