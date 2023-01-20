import binascii
from datetime import datetime
from fastapi import Depends

from ..classes.enums import AuthType
from ..dependencies.utils.token import generate_bearer_token, generate_secret, hash_password
from ..exceptions import UserNotFoundException, AuthenticationException
from ..models.repository.user import UserRepository


class AuthenticationService():

    def __init__(self,
            user_repository: UserRepository = Depends()
        ) -> None:
        self.__user_repository = user_repository

    def user_login(self, username: str, password: str) -> dict:
        user = self.__user_repository.get_user_by_email_or_username(username=username)
        if user is None:
            raise UserNotFoundException()

        check_hash, salt = hash_password(password, user.salt)

        if check_hash != binascii.unhexlify(user.hash)[:32]:
            raise AuthenticationException()

        access_key = self.__user_repository.get_access_key(user, AuthType.BEARER.value)

        current_date = datetime.now()

        if access_key:
            last_update_time = access_key.time_updated if access_key.time_updated else access_key.time_created
            time_difference = (current_date - last_update_time).seconds + (current_date - last_update_time).days * 86400

            # secret is actually the access_token field in acess_key table
            bearer_token = generate_bearer_token(user, access_key.access_token)

            if time_difference <= 3600:
                return {
                "message": "authentified",
                    "content": {
                        "token": bearer_token,
                        "token_type": AuthType.BEARER.value
                    },
                    "success": True
                }

        secret = generate_secret(user)
        user = self.__user_repository.upsert_token(user, secret)
        bearer_token = generate_bearer_token(user, secret)

        print(bearer_token)

        return {
            "message": "authentified",
            "content": {
                "token": bearer_token,
                "token_type": AuthType.BEARER.value
            },
            "success": True
        }

    def user_logout(access_token: str):
        pass
