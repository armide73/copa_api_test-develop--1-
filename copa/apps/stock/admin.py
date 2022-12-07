from django.contrib import admin
from .models import Productivity, \
    ProductivityField, ProductivityMeta

# Register your models here.
admin.site.register(Productivity)
admin.site.register(ProductivityField)
admin.site.register(ProductivityMeta)
