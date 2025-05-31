from pydantic import BaseModel

class Token(BaseModel):
    """
    Modelo de token JWT retornado após autenticação.

    Attributes:
        access_token (str): O token JWT.
        token_type (str): O tipo do token (normalmente 'bearer').
    """
    access_token: str
    token_type: str

