"""
Módulo de segurança JWT.
Geração e validação de tokens.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from jose import jwt, JWTError

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

# JWT helpers
from datetime import datetime, timedelta
from typing import Optional

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str = Depends(OAUTH2_SCHEME)) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(OAUTH2_SCHEME)) -> dict:
    payload = verify_token(token)
    return payload

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Gera um token JWT.
    Args:
        data (dict): Dados do payload.
        expires_delta (timedelta, optional): Tempo de expiração.
    Returns:
        str: Token JWT.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str = Depends(OAUTH2_SCHEME)) -> dict:
    """
    Valida o token JWT recebido.
    Args:
        token (str): Token JWT.
    Returns:
        dict: Payload decodificado.
    Raises:
        HTTPException: Se token inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
