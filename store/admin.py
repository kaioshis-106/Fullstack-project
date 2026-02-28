from django.contrib import admin
from .models import category,product
# Register your models here.

class categoryAdmin(admin.ModelAdmin):
    list_display=['category_name','slug']
    prepopulated_fields={'slug':('category_name',)}
admin.site.register(category,categoryAdmin)

class productAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    
admin.site.register(product,productAdmin)