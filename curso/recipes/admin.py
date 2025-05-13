from django.contrib import admin

from .models import Recipe, Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'author')
    list_display_links = ('title', 'created_at')
    search_fields = ('title', 'description', 'id', 'slug', 'preparation_steps')
    list_filter = (
        'is_published', 'author', 'category',
        'preparation_steps_is_html'
        )
    list_per_page = 10
    list_editable = ('is_published',)
    ordering = ('-id',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)

