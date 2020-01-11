from django.contrib import admin

from database import models as database_models


@admin.register(database_models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_filter = ["is_dummy_data"]


@admin.register(database_models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_filter = ["is_dummy_data"]


@admin.register(database_models.Journal)
class JournalAdmin(admin.ModelAdmin):
    list_filter = ["is_dummy_data"]


@admin.register(database_models.Source)
class SourceAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_filter = [
        "is_dummy_data",
        "authors",
        "source_publisher",
        "source_journal",
    ]
    raw_id_fields = ["authors", "source_publisher", "source_journal"]
