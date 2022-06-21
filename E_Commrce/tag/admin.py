from django.contrib import admin
from tag.models import TaggedItem


@admin.register(TaggedItem)
class TagAdmin(admin.ModelAdmin):
    pass
