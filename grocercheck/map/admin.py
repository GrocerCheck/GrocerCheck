from django.contrib import admin
from .models import Store
from .models import blog_entry
# Register your models here.

admin.site.register(Store)
admin.site.register(blog_entry)
