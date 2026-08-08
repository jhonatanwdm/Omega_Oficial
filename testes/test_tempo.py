from datetime import datetime, timedelta, timezone

from nucleo.tempo.servico_tempo import ServicoTempo


def test_sync_ok():
    s = ServicoTempo()
    r = s.sincronizado()
    assert r["ok"] is True
    assert r["fuso"] == "America/Sao_Paulo"


def test_drift_aviso():
    s = ServicoTempo()
    cliente = datetime.now(timezone.utc) - timedelta(minutes=5)
    inst = s.agora(cliente)
    assert inst.aviso_drift is True
