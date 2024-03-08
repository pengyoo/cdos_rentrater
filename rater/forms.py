from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django import forms

from . import models


class SignUpForm(UserCreationForm):
    email = forms.EmailField(validators=[validators.validate_email])

    min_length = 5
    max_length = 30
    message_lt_min = f"Should have at least {min_length} characters."
    message_ht_max = f"Should have at most{max_length} characters."

    username = forms.CharField(validators=[validators.MaxLengthValidator(max_length, message_ht_max),
                                           validators.MinLengthValidator(min_length, message_lt_min)])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PropertyForm(forms.ModelForm):

    class Meta:
        model = models.Property
        fields = ['address', 'area', 'property_type', 'room_type',
                  'gender_preference', 'owner_occupied', 'description']
