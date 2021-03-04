from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.


# Custom user profile
# baseusermanager determines if a user is a regular user or super user


class UserProfileManager(BaseUserManager):
    """ manager for user profiles"""

    def create_user(self, email, name, attr1, attr2, attr3, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        # make 2nd part of the email lowercase
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, attribute_one=attr1,
                          attribute_two=attr2, attribute_three=attr3)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password):
        """ create a new super user """
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in system"""
    email = models.EmailField(unique=True, max_length=254)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # by using custom user more user properties can be added
    attribute_one = models.CharField(max_length=255, null=True)
    attribute_two = models.CharField(max_length=255, null=True)
    attribute_three = models.CharField(max_length=255, null=True)

    objects = UserProfileManager()

    # Override username with email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Retrieve full name of user """
        return self.name

    def get_short_name(self):
        """ Retrieve short name of user """
        return self.name

    def __str__(self):
        return self.email
