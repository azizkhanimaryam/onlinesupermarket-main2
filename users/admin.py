from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'full_name', 'phone')

    # Updated to use email instead of username
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # No 'username' here
        ('Personal info', {'fields': ('first_name', 'last_name', 'full_name', 'phone')}),  # Added 'full_name'
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # For creating new users, ensure email and password are in the form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'full_name'),
        }),
    )

    # Using 'email' for ordering
    ordering = ['email']

    # Use 'email', 'first_name', and 'last_name' for search
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'full_name')

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'POST':
            # Log the POST data to check what's being submitted
            print("POST data: ", request.POST)

            try:
                return super().add_view(request, form_url, extra_context)
            except IntegrityError as e:
                # Log the IntegrityError for debugging
                print("IntegrityError caught: ", e)
                messages.error(request, f"Error: {e}")
                return HttpResponseRedirect(request.path_info)

        return super().add_view(request, form_url, extra_context)
    # Catch and log errors during save
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except IntegrityError as e:
            self.message_user(request, f"Integrity Error: {e}", level='error')
            raise

# Register CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
