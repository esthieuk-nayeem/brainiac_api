from django.contrib import admin
from django.contrib.auth import get_user_model


# TokenAdmin.search_fields = ['user__username']

User = get_user_model()
search_fields = ('email',)

from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token

class CustomTokenAdmin(TokenAdmin):
    search_fields = ('key', 'user__username')  # Adjust fields as per your model

admin.site.register(Token, CustomTokenAdmin)




admin.site.register(User)