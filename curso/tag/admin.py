from django.contrib import admin

# Register your models here.

from tag.models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('id', 'slug')
    search_fields = ('name', 'id', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
    list_editable = ('name',)
    ordering = ('-id',)