import dataclasses

from xpense.database.sqlite_repository import BaseRepository
from xpense.types import Transaction


@dataclasses.dataclass
class RepositoryContainer:
    transactions = BaseRepository(Transaction)
