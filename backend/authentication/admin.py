from django.contrib import admin
from authentication.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
