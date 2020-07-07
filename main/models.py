from django.db import models
import re	 # the regex module

# Create your models here.

class UserManager(models.Manager):
    def basic_validator_register(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data["first_name"]) < 2:
            errors["first_name"] = "First name needs to be at least 2 characters"

        if len(data["last_name"]) < 2:
            errors["last_name"] = "Last name needs to be at least 2 characters"

        if not EMAIL_REGEX.match(data['email']):               
            errors["email"] = "Invalid email address"

        if len(data["password"]) < 2:
            errors["password"] = "Password needs to be at least 8 characters"
        elif data["password"] != data["confirm_password"]:
            errors["password"] = "Passwords do not match"

        return errors

    def basic_validator_add_user(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(data['email']):               
            errors["email"] = "Invalid email address"

        if len(data["first_name"]) < 2:
            errors["first_name"] = "First name needs to be at least 2 characters"

        if len(data["last_name"]) < 2:
            errors["last_name"] = "Last name needs to be at least 2 characters"

        if len(data["password"]) < 2:
            errors["password"] = "Password needs to be at least 8 characters"
        elif data["password"] != data["confirm_password"]:
            errors["password"] = "Passwords do not match"

        if len(data["user_level"]) == 0:
            errors["user_level"] = "User level was not selected"

        return errors

    def basic_validator_edit_user(self, data, Session):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):               
            errors["email"] = "Invalid email address"

        if len(data["first_name"]) < 2:
            errors["first_name"] = "First name needs to be at least 2 characters"

        if len(data["last_name"]) < 2:
            errors["last_name"] = "Last name needs to be at least 2 characters"

        if User.objects.get(id=Session["user_id"]).level == 9:
            if len(data["user_level"]) == 0:
                errors["user_level"] = "User level was not selected"

        return errors

    def basic_validator_update_password(self, data):
        errors = {}

        if len(data["password"]) < 2:
            errors["password"] = "Password needs to be at least 8 characters"
        elif data["password"] != data["confirm_password"]:
            errors["password"] = "Passwords do not match"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 45)
    level =  models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="messages_posted", on_delete = models.CASCADE)
    recipient = models.ForeignKey(User, related_name="messages_posted_to", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name="comments_posted", on_delete = models.CASCADE)
    recipient = models.ForeignKey(User, related_name="comments_posted_to", on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments_posted", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)