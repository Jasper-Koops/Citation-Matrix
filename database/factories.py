import random
from datetime import timedelta
from typing import Optional

import factory
from django.utils import timezone
from faker import Faker

from database import models as database_models

fake = Faker()


class AuthorFactory(factory.DjangoModelFactory):
    class Meta:
        model = database_models.Author

    is_dummy_data = True
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @factory.lazy_attribute
    def middle_name(self) -> Optional[factory.Faker]:
        """ Authors have a 50% chance of having a middle name """
        if random.random() > 0.00001:
            return fake.first_name()
        return None


class PublisherFactory(factory.DjangoModelFactory):
    class Meta:
        model = database_models.Publisher

    is_dummy_data = True
    name = factory.Faker("company")
    city = factory.Faker("city")


class JournalFactory(factory.DjangoModelFactory):
    class Meta:
        model = database_models.Journal

    is_dummy_data = True
    name = factory.Faker("company")
    journal_publisher = factory.SubFactory(PublisherFactory)


# FIXME - dat property ding hier toepassen
class SourceFactory(factory.DjangoModelFactory):
    class Meta:
        model = database_models.Source

    is_dummy_data = True
    title = factory.Faker("sentence")
    source_publisher = None
    year_of_publication = factory.LazyFunction(
        lambda: random.randint(1950, 2020)
    )
    type = "AR"
    source_journal = factory.SubFactory(JournalFactory)
    abstract = factory.Faker("text")

    @factory.lazy_attribute
    def journal_page_range_start(self) -> int:
        return random.randint(1, 100)

    @factory.lazy_attribute
    def journal_page_range_end(self) -> int:
        article_length: int = random.randint(1, 30)
        return self.journal_page_range_start + article_length

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of seasons were passed in, use them
            for a in extracted:
                self.authors.add(a)

    class Params:
        article = factory.Trait(
            type="AR",
            source_publisher=None,
            source_journal=factory.SubFactory(JournalFactory),
        )
        book = factory.Trait(
            type="BK",
            source_publisher=factory.SubFactory(PublisherFactory),
            source_journal=None,
        )


class ReferenceFactory(factory.DjangoModelFactory):
    class Meta:
        model = database_models.Reference

    is_dummy_data = True
    referrer = factory.SubFactory(SourceFactory)
    reference = factory.SubFactory(SourceFactory)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = "database.User"

    username = factory.Sequence(lambda n: "user_%d" % n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("first_name")
    email = factory.Faker("email")
    is_active = True
    is_staff = False
    is_superuser = False
    last_login = factory.LazyFunction(timezone.now)

    @factory.lazy_attribute
    def date_joined(self):
        return timezone.now() - timedelta(days=random.randint(10, 20))

    class Params:
        is_super = factory.Trait(is_staff=True, is_superuser=True)


class EvaluationFactory(factory.DjangoModelFactory):
    class Meta:
        model = database_models.Evaluation

    is_dummy_data = True
    user = factory.SubFactory(UserFactory)
    source = factory.SubFactory(SourceFactory)
    date = factory.LazyFunction(timezone.now)
    comments = factory.Faker("text")
    favorited = False
