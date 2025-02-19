from django.contrib import admin

from .models import Recipe, Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)

