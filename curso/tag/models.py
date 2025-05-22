from random import SystemRandom
import string

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join([SystemRandom().choice(
                string.ascii_letters + string.digits,
                ) for _ in range(6)])
            self.slug = slugify(f'{self.name}-{rand_letters}')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
