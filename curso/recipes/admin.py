from django.contrib import admin

from .models import Recipe, Category
# from tag.models import Tag

# from django.contrib.contenttypes.admin import GenericStackedInline

# Register your models here.


# class TagInline(GenericStackedInline):
#     model = Tag
#     extra = 1
#     fields = ('name',)


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
    autocomplete_fields = ('tags',)

    # inlines = (TagInline,)


admin.site.register(Category, CategoryAdmin)
