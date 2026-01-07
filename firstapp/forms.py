from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.core.exceptions import ValidationError
from .models import Profile, Item, Order

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=[('shopkeeper', 'Shopkeeper'), ('customer', 'Customer')],
        required=True,
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "user_type")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        existing_usernames = set(User.objects.values_list("username", flat=True))

        if username in existing_usernames:
            raise ValidationError("This username is already taken. Please choose a different one.")

        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.user_type = self.cleaned_data['user_type']
            profile.save()
            if profile.user_type == 'shopkeeper':
                group = Group.objects.get(name='shopkeeper')
            else:
                group = Group.objects.get(name='customer')

            user.groups.add(group)  

        return user

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'quantity', 'price']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['item', 'quantity']
