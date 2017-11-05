from django.contrib import admin
from .models import Author,KeyWord,Documents
# Register your models here.
admin.site.register(Author)
admin.site.register(KeyWord)
admin.site.register(Documents)
