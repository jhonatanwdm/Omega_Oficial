from nucleo.voz.wake_word import DetectorWakeWord


def test_wake_word_detecta_e_residual():
    d = DetectorWakeWord()
    r = d.avaliar("Omega, ligue as luzes")
    assert r.detectado is True
    assert "luzes" in r.residual.lower()


def test_wake_word_negativo():
    d = DetectorWakeWord()
    r = d.avaliar("bom dia assistente")
    assert r.detectado is False
