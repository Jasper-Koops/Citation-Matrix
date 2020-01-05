from django.test import TestCase

from database.factories import AuthorFactory, JournalFactory, PublisherFactory
from database.models import Author, Journal, Publisher


class TestAuthorModel(TestCase):
    def setUp(self) -> None:
        self.author: Author = AuthorFactory()

    def test_init(self) -> None:
        self.assertTrue(self.author)
        self.assertTrue(
            self.author.first_name[0] in self.author.initials_of_first_names
        )


class TestPublisherModel(TestCase):
    def setUp(self) -> None:
        self.publisher: Publisher = PublisherFactory()

    def test_init(self) -> None:
        self.assertTrue(self.publisher)


class TestJournalModel(TestCase):
    def setUp(self) -> None:
        self.journal: Journal = JournalFactory()

    def test_init(self) -> None:
        self.assertTrue(self.journal)
