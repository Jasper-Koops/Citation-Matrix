from django.test import TestCase

from database.factories import (
    AuthorFactory,
    JournalFactory,
    PublisherFactory,
    ReferenceFactory,
    SourceFactory,
)
from database.models import Author, Journal, Publisher, Reference, Source


class TestAuthorModel(TestCase):
    def setUp(self) -> None:
        self.author: Author = AuthorFactory()

    def test_init(self) -> None:
        self.assertTrue(self.author)
        self.assertTrue(self.author.is_dummy_data)

    def test__str__(self) -> None:
        self.assertEqual(
            str(self.author),
            "{} {} {}".format(
                self.author.first_name,
                self.author.middle_name,
                self.author.last_name,
            ),
        )

    def test_initials_of_first_and_middle_names_property(self) -> None:
        author: Author = AuthorFactory(
            first_name="Jan Peter", middle_name="Fred Arnold"
        )
        self.assertEqual(author.initials_of_first_and_middle_names, "J P F A")


class TestPublisherModel(TestCase):
    def setUp(self) -> None:
        self.publisher: Publisher = PublisherFactory()

    def test_init(self) -> None:
        self.assertTrue(self.publisher)
        self.assertTrue(self.publisher.is_dummy_data)

    def test__str__(self) -> None:
        self.assertEqual(
            str(self.publisher), "{}".format(self.publisher.name,),
        )


class TestJournalModel(TestCase):
    def setUp(self) -> None:
        self.journal: Journal = JournalFactory()

    def test_init(self) -> None:
        self.assertTrue(self.journal)
        self.assertTrue(self.journal.is_dummy_data)

    def test__str__(self) -> None:
        self.assertEqual(
            str(self.journal), "{}".format(self.journal.name,),
        )


class TestSourceModel(TestCase):
    def setUp(self) -> None:
        self.source: Source = SourceFactory()

    def test_init(self) -> None:
        self.assertTrue(self.source)
        self.assertTrue(self.source.is_dummy_data)

    def test__str__(self) -> None:
        self.assertEqual(
            str(self.source),
            "{} ({})".format(self.source.title, self.source.type),
        )

    def test_book_trait(self) -> None:
        article: Source = SourceFactory(article=True)
        self.assertEqual(article.type, "AR")
        self.assertEqual(article.source_publisher, None)
        self.assertNotEqual(article.source_journal, None)

    def test_article_trait(self) -> None:
        book: Source = SourceFactory(book=True)
        self.assertEqual(book.type, "BK")
        self.assertNotEqual(book.source_publisher, None)
        self.assertEqual(book.source_journal, None)

    def test_get_publisher_property_for_books(self) -> None:
        publisher: Publisher = PublisherFactory()
        book: Source = SourceFactory(book=True, source_publisher=publisher)
        self.assertEqual(book.get_publisher, publisher)

    def test_get_publisher_property_for_articles(self) -> None:
        publisher: Publisher = PublisherFactory()
        journal: Journal = JournalFactory(journal_publisher=publisher)
        article: Source = SourceFactory(article=True, source_journal=journal)
        self.assertEqual(article.get_publisher, publisher)

    def test_save_journal_page_check(self) -> None:
        with self.assertRaisesMessage(
            ValueError, "Invalid page range! Start is placed after the end!"
        ):
            SourceFactory(journal_page_range_start=5, journal_page_range_end=3)

    def test_save_book_journal_check(self) -> None:
        with self.assertRaisesMessage(
            ValueError,
            "Source with type 'book' cannot be linked to a journal!",
        ):
            SourceFactory(book=True, source_journal=JournalFactory())

    def test_save_book_publisher_check(self) -> None:
        with self.assertRaisesMessage(
            ValueError, "Source with type 'book' has no publisher set!"
        ):
            SourceFactory(book=True, source_publisher=None)

    def test_save_article_journal_check(self) -> None:
        with self.assertRaisesMessage(
            ValueError, "Article is not linked to a journal!"
        ):
            SourceFactory(article=True, source_journal=None)

    def test_save_article_publisher_check(self) -> None:
        with self.assertRaisesMessage(
            ValueError,
            "Source with type 'article' has a publisher set! "
            "(Should be done in the journal instead)",
        ):
            SourceFactory(article=True, source_publisher=PublisherFactory())


class TestReferenceModel(TestCase):
    def setUp(self) -> None:
        self.reference: Reference = ReferenceFactory()

    def test_init(self) -> None:
        self.assertTrue(self.reference)
        self.assertTrue(self.reference.is_dummy_data)

    def test__str__(self) -> None:
        self.assertEqual(
            str(self.reference),
            "{} - {}".format(
                self.reference.referrer, self.reference.reference
            ),
        )
