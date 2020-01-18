from django.core.management.base import BaseCommand
from django.db.models import QuerySet

from database.factories import (
    AuthorFactory,
    EvaluationFactory,
    JournalFactory,
    PublisherFactory,
    ReferenceFactory,
    SourceFactory,
    UserFactory,
)
from database.models import (
    Author,
    Evaluation,
    Journal,
    Publisher,
    Reference,
    Source,
    User,
)


class Command(BaseCommand):
    help = "Generates dummy data for the application database."

    def generate_users(self) -> None:
        """ Generates 5 users """
        for x in range(5):
            user: User = UserFactory()
            self.stdout.write(
                self.style.SUCCESS("Created user: {}").format(user)
            )

    def generate_publishers(self) -> None:
        """ Generates 5 fake publishers """
        for x in range(5):
            publisher: Publisher = PublisherFactory()
            self.stdout.write(
                self.style.SUCCESS("Created publisher: {}").format(publisher)
            )

    def generate_journals(self) -> None:
        """ Generates 3 fake journals for each publisher """
        for publisher in Publisher.objects.all():
            for x in range(3):
                journal: Journal = JournalFactory(journal_publisher=publisher)
                self.stdout.write(
                    self.style.SUCCESS("Created journal: {}").format(journal)
                )

    def generate_authors(self) -> None:
        """ Generates 20 authors """
        for x in range(20):
            author: Author = AuthorFactory()
            self.stdout.write(
                self.style.SUCCESS("Created author: {}").format(author)
            )

    def generate_books(self) -> None:
        """ Have each author write 2 books """
        for author in Author.objects.all():
            for x in range(2):
                selected_publisher: Publisher = Publisher.objects.all().order_by(
                    "?"
                ).first()
                book: Source = SourceFactory(
                    book=True,
                    source_publisher=selected_publisher,
                    authors=[author],
                )
                self.stdout.write(
                    self.style.SUCCESS("Created book: {}").format(book)
                )

    def generate_articles_single_author(self) -> None:
        """ Have each author write 3 articles """
        for author in Author.objects.all():
            for x in range(3):
                selected_journal: Journal = Journal.objects.all().order_by(
                    "?"
                ).first()
                article: Source = SourceFactory(
                    article=True,
                    source_journal=selected_journal,
                    authors=[author],
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "Created article (single author): {}"
                    ).format(article)
                )

    def generate_articles_two_authors(self) -> None:
        """
        Have each author team up with another and write two articles together
        """
        queryset: QuerySet[Author] = Author.objects.all()
        author_iterator = iter(queryset)
        for author_1 in author_iterator:
            selected_journal: Journal = Journal.objects.all().order_by(
                "?"
            ).first()
            article: Source = SourceFactory(
                article=True,
                source_journal=selected_journal,
                authors=[author_1, next(author_iterator)],
            )
            self.stdout.write(
                self.style.SUCCESS(
                    "Created article (multiple authors): {}"
                ).format(article)
            )

    def generate_super_user(self) -> None:
        """
        Generates the superuser, with default (and very insecure) email and
        password
        """
        terrible_superuser_credentials: str = "test"
        superuser: User = User.objects.create_user(
            # “The way to a man’s heart is through his chest!”
            first_name="cheradenine",
            last_name="zakalwe",
            username="test",
            password=terrible_superuser_credentials,
        )
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save()
        self.stdout.write(
            self.style.SUCCESS("Created default superuser: {}").format(
                superuser
            )
        )

    def generate_references(self) -> None:
        """ Generates 400 references """
        for x in range(400):
            randomized_sources: QuerySet[
                Source
            ] = Source.objects.all().order_by("?")
            referrer: Source = randomized_sources.first()
            reference: Source = randomized_sources.last()
            reference_object: Reference = ReferenceFactory(
                referrer=referrer, reference=reference
            )
            self.stdout.write(
                self.style.SUCCESS("Created reference: {}").format(
                    reference_object
                )
            )

    def generate_evaluations(self) -> None:
        """ Generates 8 evaluations for random sources for each user """
        for user in User.objects.all():
            for x in range(8):
                selected_source: Source = Source.objects.all().order_by(
                    "?"
                ).first()
                evaluation: Evaluation = EvaluationFactory(
                    user=user, source=selected_source
                )
                self.stdout.write(
                    self.style.SUCCESS("Created {}").format(evaluation)
                )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Generating dummy data!"))
        self.generate_users()
        self.generate_publishers()
        self.generate_journals()
        self.generate_authors()
        self.generate_books()
        self.generate_articles_single_author()
        self.generate_articles_two_authors()
        self.generate_references()
        self.generate_super_user()
        self.generate_evaluations()
        self.stdout.write(self.style.SUCCESS("Done"))
