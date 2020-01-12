from django.contrib import admin

from database import models as database_models


@admin.register(database_models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "middle_name", "last_name"]
    list_filter = ["is_dummy_data"]
    search_fields = ["first_name", "middle_name", "last_name"]


@admin.register(database_models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name", "city"]
    list_filter = ["is_dummy_data", "city"]
    search_fields = ["name"]


@admin.register(database_models.Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ["name", "journal_publisher"]
    list_filter = ["is_dummy_data", "journal_publisher"]
    search_fields = ["name"]
    raw_id_fields = ["journal_publisher"]


@admin.register(database_models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "type",
        "year_of_publication",
        "source_publisher",
        "source_journal",
    ]
    list_filter = [
        "is_dummy_data",
        "type",
        "authors",
        "source_publisher",
        "source_journal",
    ]
    search_fields = ["title"]
    raw_id_fields = ["authors", "source_publisher", "source_journal"]
