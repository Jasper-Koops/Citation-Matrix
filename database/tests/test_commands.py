from django.core.management import call_command
from django.db.models import Count
from django.test import TestCase

from database.models import Author, Journal, Publisher, Source


class TestGenerateDummyDataCommand(TestCase):
    def verify_publishers(self) -> None:
        """ Verify that the publishers have been created as planned. """
        self.assertEqual(Publisher.objects.all().count(), 5)

    def verify_journals(self) -> None:
        """ Verify that the Journals have been created as planned. """
        self.assertEqual(Journal.objects.all().count(), 15)
        for journal in Journal.objects.all():
            self.assertTrue(
                journal.journal_publisher in Publisher.objects.all()
            )

    def verify_authors(self) -> None:
        """ Verify that the authors have been created as planned. """
        self.assertEqual(Author.objects.all().count(), 20)

    def verify_books(self) -> None:
        """ Verify that the books have been created as planned. """
        self.assertEqual(Source.objects.filter(type="BK").count(), 40)

    def verify_single_author_articles(self) -> None:
        """
        Verify that the (single author) articles have been created as planned.
        """
        self.assertEqual(
            Source.objects.annotate(num_authors=Count("authors"))
            .filter(type="AR", num_authors=1)
            .count(),
            60,
        )

    def verify_multiple_author_articles(self) -> None:
        """
        Verify that the (multiple author) articles have been created as planned.
        """
        self.assertEqual(
            Source.objects.annotate(num_authors=Count("authors"))
            .filter(type="AR", num_authors=2)
            .count(),
            10,
        )

    def test_command(self) -> None:
        # Call command
        call_command("generate_dummy_data")
        self.verify_publishers()
        self.verify_journals()
        self.verify_authors()
        self.verify_books()
        self.verify_single_author_articles()
        self.verify_multiple_author_articles()
