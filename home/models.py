from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify  
from ckeditor.fields import RichTextField

# Create your models here.

SUBSCRIPTION = (
    ('F' , 'FREE'),
    ('M' , 'MONTHLY'),
    ('Y' , 'YEARLY'),
    )


class Profile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    is_pro = models.BooleanField(default=False)
    pro_expiry_date = models.DateField(null=True, blank=True)
    subscription_type = models.CharField(max_length=100 , choices=SUBSCRIPTION , default='FREE')
    
    


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_description = RichTextField()
    is_premium = models.BooleanField(default=False)
    course_image = models.ImageField(upload_to="course")
    video_link = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(blank=True)
    
    
    def save(self,*args, **kwargs): 
        self.slug = slugify(self.course_name)
        super(Course, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.course_name
    


class CourseModule(models.Model):
    course = models.ForeignKey(Course , on_delete=models.CASCADE)
    course_module_name = models.CharField(max_length=100)
    course_description =RichTextField()
    video_url = models.URLField(max_length=200)
    can_view = models.BooleanField(default=False)




class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self) -> str:
        return 'massage from' + self.name + '-' + self.email

class Signup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=500, blank=False)    

    
    