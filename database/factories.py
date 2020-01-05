import random
from typing import Optional

import factory
from faker import Faker

from database import models as database_models

fake = Faker()


class AuthorFactory(factory.DjangoModelFactory):
    class Meta:
        model = database_models.Author

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @factory.lazy_attribute
    def middle_name(self) -> Optional[factory.Faker]:
        """ Authors have a 50% chance of having a middle name """
        if random.random() > 0.00001:
            return fake.first_name()
        return None

    @factory.lazy_attribute
    def initials_of_first_names(self) -> str:
        """ Fetch the initials from the first name and optional middle name """
        first_name_initials: str = self.first_name[0].upper()
        if self.middle_name:
            middle_name_initials: str = self.middle_name[0].upper()
            return "{} {}".format(first_name_initials, middle_name_initials)
        return first_name_initials


class PublisherFactory(factory.DjangoModelFactory):
    class Meta:
        model = database_models.Publisher

    name = factory.Faker("company")
    city = factory.Faker("city")


class JournalFactory(factory.DjangoModelFactory):
    class Meta:
        model = database_models.Journal

    name = factory.Faker("company")


class SourceFactory(factory.DjangoModelFactory):
    class Meta:
        model = database_models.Source

    title = factory.Faker("sentence")
    authors = None
    publisher = None
    year_of_publication = factory.LazyFunction(
        lambda: random.randint(1950, 2020)
    )
    journal = factory.SubFactory(JournalFactory)
    journal_page_range_start = None
    journal_page_range_end = None
