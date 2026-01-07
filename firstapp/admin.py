from django.contrib import admin
from .models import User, Item, Order

admin.site.register(Item)
admin.site.register(Order)

from .forms import NewUserForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = NewUserForm
    model = User

    fieldsets = UserAdmin.fieldsets  

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
