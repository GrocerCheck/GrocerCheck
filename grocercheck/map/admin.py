from django.contrib import admin
from .models import Store
from .models import blog_entry
from .models import ad_placement
# Register your models here.

admin.site.register(ad_placement)
admin.site.register(Store)
admin.site.register(blog_entry)
