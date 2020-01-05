from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    initials_of_first_names = models.CharField(
        max_length=10, blank=True, null=True
    )


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200, blank=True, null=True)


class Journal(models.Model):
    name = models.CharField(max_length=200)


class Source(models.Model):
    title = models.CharField(max_length=400)
    authors = models.ManyToManyField(Author, related_name="sources")
    publisher = models.ForeignKey(
        Publisher,
        related_name="sources",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    year_of_publication = models.IntegerField()
    journal = models.ForeignKey(
        Journal, blank=True, null=True, on_delete=models.CASCADE
    )
    journal_page_range_start = models.PositiveIntegerField(
        blank=True, null=True
    )
    journal_page_range_end = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Verify that journal_page_range, if provided, has valid values """
        if self.journal_page_range_start and self.journal_page_range_end:
            if self.journal_page_range_start < self.journal_page_range_end:
                raise ValueError(
                    "Invalid page range! Start cannot be lower than end!"
                )
        super(Source, self).save(*args, **kwargs)
