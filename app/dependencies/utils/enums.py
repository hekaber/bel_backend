from enum import Enum

class AuthType(Enum):
    BEARER = 'bearer'
    OAUTH2 = 'oauth2'
    DUAL = 'dual'