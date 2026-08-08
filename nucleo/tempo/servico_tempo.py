from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pendulum

from nucleo.comum.config import get_configs


@dataclass
class Instantaneo:
    utc: datetime
    local: datetime
    fuso: str
    iso_utc: str
    iso_local: str
    drift_segundos: float | None = None
    aviso_drift: bool = False


class ServicoTempo:
    def __init__(self) -> None:
        pol = get_configs()["politicas"]["tempo"]
        self.fuso_exibicao = pol["exibicao"]
        self.limiar_drift = float(pol["limiar_drift_segundos"])
        self._tz = ZoneInfo(self.fuso_exibicao)

    def agora(self, relogio_cliente_utc: datetime | None = None) -> Instantaneo:
        utc = datetime.now(timezone.utc)
        local = utc.astimezone(self._tz)
        drift = None
        aviso = False
        if relogio_cliente_utc is not None:
            if relogio_cliente_utc.tzinfo is None:
                relogio_cliente_utc = relogio_cliente_utc.replace(tzinfo=timezone.utc)
            drift = abs((utc - relogio_cliente_utc).total_seconds())
            aviso = drift > self.limiar_drift
        return Instantaneo(
            utc=utc,
            local=local,
            fuso=self.fuso_exibicao,
            iso_utc=utc.isoformat(),
            iso_local=local.isoformat(),
            drift_segundos=drift,
            aviso_drift=aviso,
        )

    def para_exibicao(self, dt_utc: datetime) -> str:
        if dt_utc.tzinfo is None:
            dt_utc = dt_utc.replace(tzinfo=timezone.utc)
        return dt_utc.astimezone(self._tz).isoformat()

    def sincronizado(self) -> dict:
        agora = self.agora()
        # Confia no NTP do SO; valida consistência interna com pendulum
        p = pendulum.now("UTC")
        drift_interno = abs((agora.utc - p).total_seconds())
        return {
            "fonte": "sistema_operacional_ntp",
            "utc": agora.iso_utc,
            "local": agora.iso_local,
            "fuso": self.fuso_exibicao,
            "drift_interno_segundos": drift_interno,
            "ok": drift_interno < self.limiar_drift,
        }
