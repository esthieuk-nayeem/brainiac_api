from django.contrib import admin
from django.contrib.auth import get_user_model


# TokenAdmin.search_fields = ['user__username']

User = get_user_model()
search_fields = ('email',)






admin.site.register(User)