from __future__ import annotations

from dataclasses import dataclass

from fastapi import Header, HTTPException, status

from nucleo.comum.config import get_settings


@dataclass
class Autorizacao:
    valido: bool
    papel: str = "desenvolvedor"


def verificar_token_dev(token: str | None) -> Autorizacao:
    esperado = get_settings().omega_token_dev
    if not token or token != esperado:
        return Autorizacao(valido=False)
    return Autorizacao(valido=True, papel="desenvolvedor")


async def exigir_dev(
    x_omega_token: str | None = Header(default=None, alias="X-Omega-Token"),
) -> Autorizacao:
    auth = verificar_token_dev(x_omega_token)
    if not auth.valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token do desenvolvedor inválido ou ausente",
        )
    return auth
