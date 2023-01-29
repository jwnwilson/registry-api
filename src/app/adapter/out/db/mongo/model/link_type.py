from app.domain.link_type import LinkTypeDTO
from ..repository import MongoRepository


class LinkTypeRepository(MongoRepository):
    model_dto = LinkTypeDTO
    table = "linkType"

