from .base import BaseRepository
from ...models.orm.auth import AccessKey

class AuthRepository(BaseRepository):

    def remove_access(self, access_key: AccessKey):
        self.db.delete(access_key)
        self.db.commit()