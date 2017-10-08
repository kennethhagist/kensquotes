# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        user = None
        if not self.filter(email=post_data['email']):
            errors.append("Invalid email/password")
        else:
            user = self.get(email=post_data['email'])
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append("Invalid email/password")
        
        return errors, user

    def validate_registration(self, post_data):
        errors = []
        user = None
        for field, value in post_data.iteritems():
            if len(value) < 1:
                errors.append("All fields are required")
                break

        if len(post_data['name']) < 3:
            errors.append("Name field must be 3 or more")
        if len(post_data['password']) < 8:
            errors.append("Password  must be 8 or more characters")
        if post_data['password'] != post_data['password_confirm']:
            errors.append("password does not match")
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append("name must be letter characters only")
        if len(post_data['alias']) < 3:
            errors.append("Alias must be at least 3 characters")
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("Email already in use")
        
        if not errors:
            hashed_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())

            user = self.create(
                name = post_data['name'],
                alias = post_data['alias'],
                email = post_data['email'],
                date_of_birth = post_data['date_of_birth'],
                password = hashed_pw
            )            
        return errors, user

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth= models.DateField()
    password = models.CharField(max_length=250)
    objects = UserManager()
    def __str__(self):
        return "{}".format(self.alias)

class QuoteManager(models.Manager):
    def validate_quote(self, quote_text, current_user_id, quoted_by):
        errors = []
        if len(quoted_by) < 4:
            msg = "'Quoted by' is not just for man, Shakespeare had more than 3 characters!!"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(quote_text) < 11:
            msg = "To be or not to be, for thou shan't be too short 10 characters the rapper!"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        current_user = User.objects.get(id = current_user_id)
        self.create(quote_text = quote_text, author = current_user, quoted_by = quoted_by)
        msg = "Quotage maketh man!"
        errors.append(msg)
        result = {'status' : True, 'errors' : errors[0]}
        return result

    def likes(self, user_id, quote_id):       
        quote = Quote.objects.get(id = quote_id)
        current_user = User.objects.get(id = user_id)
        quote.likes_users.add(current_user)
        result = {'status': True}
        return result
    
    def remove(self, user_id, quote_id):
        quote = Quote.objects.get(id = quote_id)
        current_user = User.objects.get(id = user_id)
        quote.likes_users.remove(current_user)

    # def contribute_quotes(self, clean_data, user_id):
    #     return self.create(
    #         author = quoted_by,
    #         quote = massage,
    #         created_at = models.DateTimeField(auto_now_add=True),
    #         postman = User.objects.get(id=user_id)
    #     )

    # def recent_and_not(self):
    #     return (self.all().order_by('-created_at')[:3], self.all().order_by('-created_at')[3:])

class Quote(models.Model):
    quote_text = models.TextField(max_length = 1000, null = True)
    author = models.ForeignKey(User, related_name="quotes_posted")
    quoted_by = models.CharField (max_length=255, null = True)
    likes_user = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    objects = QuoteManager()
    def __str__(self):
        return "Quote: {}".format(self.quote.title)