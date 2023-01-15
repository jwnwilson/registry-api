import factory
import pytest

from app.adapter.db import model


@pytest.fixture
def property_factory(db):
    class PropertyFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = model.Property
            sqlalchemy_session = db.session

        street_name = factory.Faker("street_address")
        postal_code = factory.Faker("postcode")
        city = factory.Faker("city")
        county = factory.Faker("city_suffix")
        state_code = "AZ"
        country = "US"

    return PropertyFactory
