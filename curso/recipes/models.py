import os

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from PIL import Image

from tag.models import Tag


def resize_image(image, new_width=850):
    image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)

    image_pillow = Image.open(image_full_path)
    original_width, original_height = image_pillow.size

    if original_width <= new_width:
        image_pillow.close()
        return

    new_height = round((new_width * original_height) / original_width)

    new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)\

    new_image.save(
        image_full_path,
        optimize=True,
        quality=60
    )


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True)


class Recipe(models.Model):
    title = models.CharField(max_length=65, verbose_name=_('title'))
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/',
        null=True, blank=True
        )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True, default=None
        )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True, default='')

    #tags = GenericRelation(Tag, related_query_name='recipes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id, ))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        _super = super().save(*args, **kwargs)

        if self.cover:
            resize_image(self.cover)

        return _super
