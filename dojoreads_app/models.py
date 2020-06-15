from django.db import models
import re


class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Your name and alias must be at least 2 characters"
        if len(postData['alias']) < 2:
            errors['alias'] = "Alias must be 2 or more characters"
        if len(postData['email']) == 0:
            errors['email_e'] = "Email field cannot be blank"
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_checker.match(postData['email']):
            errors['email'] = "Email must be valid"
        result = User.objects.filter(email=postData['email'])
        if result:
            errors['email_f'] = "Email address is already registered"
        if len(postData['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters"
        if postData['pw'] != postData['conf_pw']:
            errors['conf_pw'] = "Password and Confirm password must match"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField(default=0)
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    poster = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
