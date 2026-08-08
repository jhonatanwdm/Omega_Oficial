from nucleo.comum.config import get_settings
from nucleo.politicas.motor_politicas import MotorPoliticas


def test_cloud_desligada_por_padrao():
    settings = get_settings()
    anterior = settings.cloud_llm_habilitada
    settings.cloud_llm_habilitada = False
    try:
        m = MotorPoliticas()
        dec = m.avaliar("usar_llm_cloud", confirmado=True)
        assert dec.permitido is False
    finally:
        settings.cloud_llm_habilitada = anterior


def test_nao_pode_shell_livre():
    m = MotorPoliticas()
    dec = m.avaliar("shell_livre")
    assert dec.permitido is False


def test_conversar_texto_ok():
    m = MotorPoliticas()
    dec = m.avaliar("conversar_texto")
    assert dec.permitido is True


def test_allowlist_caminho():
    m = MotorPoliticas()
    assert m.caminho_permitido(r"C:\Mundo_Web_Antigo\Omega\dados\x.txt")
    assert not m.caminho_permitido(r"C:\Windows\System32\config")
