from typing import Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    pass


class CMBaseModel(models.Model):
    is_dummy_data = models.BooleanField(
        default=False, verbose_name=_("Instance was generated as dummy data")
    )

    class Meta:
        abstract = True


class Author(CMBaseModel):
    first_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_("First name of the author"),
    )
    middle_name = models.CharField(
        max_length=200,
        verbose_name=_("Middle name(s) of the author"),
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=200, verbose_name=_("Last name of the author")
    )

    def __str__(self) -> str:
        return "{} {} {}".format(
            self.first_name, self.middle_name, self.last_name
        )

    @property
    def initials_of_first_and_middle_names(self):
        """
        Returns the Initials of the author.
        (based on the values of the 'first_name' and 'middle_name' fields
        """
        initials_of_first_names: str = " ".join(
            [name[0].upper() for name in self.first_name.split()]
        )
        initials_of_middle_names: str = " ".join(
            [name[0].upper() for name in self.middle_name.split()]
        )
        return initials_of_first_names + " " + initials_of_middle_names


class Publisher(CMBaseModel):
    name = models.CharField(
        max_length=200, verbose_name=_("Name of the publisher")
    )
    city = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_("City the publisher is located in"),
    )

    def __str__(self) -> str:
        return "{}".format(self.name)


class Journal(CMBaseModel):
    name = models.CharField(
        max_length=200, verbose_name=_("Name of the journal")
    )
    journal_publisher = models.ForeignKey(
        Publisher,
        related_name="journals",
        verbose_name=_("Publisher of the journal"),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return "{}".format(self.name)


class Source(CMBaseModel):
    TYPE_CHOICES: Tuple[Tuple[str, str], ...] = (
        ("AR", "Article"),
        ("BK", "Book"),
    )

    title = models.CharField(
        max_length=400, verbose_name=_("Title of the source")
    )
    authors = models.ManyToManyField(
        Author, related_name="sources", verbose_name=_("Authors of the source")
    )
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="AR",
        verbose_name=_("Type of the source"),
    )
    source_publisher = models.ForeignKey(
        Publisher,
        related_name="books",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Publisher of the source (if applicable)"),
    )
    year_of_publication = models.IntegerField(
        verbose_name=_("Publisher of the source")
    )
    source_journal = models.ForeignKey(
        Journal,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Journal the source was published in (if applicable)"),
    )
    journal_page_range_start = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Index of the journal page where the article begins."),
    )
    journal_page_range_end = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Index of the journal page where the article ends."),
    )
    abstract = models.TextField(
        blank=True, null=True, verbose_name=_("The abstract of the source.")
    )

    def __str__(self) -> str:
        return "{} ({})".format(self.title, self.type)

    @property
    def get_publisher(self):
        """
        Returns the publisher on the source, based on the values of its
        'source_publisher' and 'source_journal' fields.
        """
        if self.source_publisher:
            return self.source_publisher
        return self.source_journal.journal_publisher

    def save(self, *args, **kwargs):
        """
        Runs the following checks before saving:
        - Verify that journal_page_range, if provided, has valid values
        - Verify that sources with type 'book' has a publisher set
        - Verify that sources with type 'book' don't have journal set.
        - Verify that sources with type 'article' don't have a publisher set
        - Verify that sources with type 'article' are linked to a journal.
        """
        # Page range check
        if self.journal_page_range_start and self.journal_page_range_end:
            if self.journal_page_range_start > self.journal_page_range_end:
                raise ValueError(
                    "Invalid page range! Start is placed after the end!"
                )

        # Book checks
        if self.type == "BK":
            if self.source_journal:
                raise ValueError(
                    "Source with type 'book' cannot be linked to a journal!"
                )
            if not self.source_publisher:
                raise ValueError(
                    "Source with type 'book' has no publisher set!"
                )

        # article checks
        if self.type == "AR":
            if not self.source_journal:
                raise ValueError("Article is not linked to a journal!")
            if self.source_publisher:
                raise ValueError(
                    "Source with type 'article' has a publisher set! "
                    "(Should be done in the journal instead)"
                )

        super(Source, self).save(*args, **kwargs)


class Reference(CMBaseModel):
    referrer = models.ForeignKey(
        Source,
        related_name="citations",
        on_delete=models.CASCADE,
        verbose_name=_("The source making the reference ('FROM')"),
    )
    reference = models.ForeignKey(
        Source,
        related_name="cited",
        on_delete=models.CASCADE,
        verbose_name=_("The source being referred to ('TO')"),
    )

    def __str__(self) -> str:
        return "{} - {}".format(self.referrer, self.reference)


class Evaluation(CMBaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User making the evaluation"),
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        verbose_name=_("The source being evaluated"),
    )
    date = models.DateField(
        default=timezone.now, verbose_name=_("Date of the evaluation.")
    )
    comments = models.TextField(
        blank=True, null=True, verbose_name=_("Comments made by the user")
    )
    favorited = models.BooleanField(
        default=False,
        verbose_name=_(
            "A boolean indicating if the source has been favorited by the user."
        ),
    )

    def __str__(self) -> str:
        return "Evaluation for {} from {}".format(self.source, self.user)
