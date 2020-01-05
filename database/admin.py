from django.contrib import admin

from database import models as database_models


@admin.register(database_models.Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(database_models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass


@admin.register(database_models.Journal)
class JournalAdmin(admin.ModelAdmin):
    pass


@admin.register(database_models.Source)
class SourceAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_filter = ["authors", "publisher", "journal"]
    raw_id_fields = ["authors", "publisher", "journal"]
