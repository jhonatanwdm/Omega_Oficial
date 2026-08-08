from fastapi.testclient import TestClient

from nucleo.api.principal import app


def test_saude_e_chat():
    with TestClient(app) as client:
        s = client.get("/saude")
        assert s.status_code == 200
        assert s.json()["ok"] is True

        ui = client.get("/")
        assert ui.status_code == 200
        assert "Omega" in ui.text

        css = client.get("/ui/estilos.css")
        assert css.status_code == 200

        negado = client.post("/chat", json={"texto": "oi"})
        assert negado.status_code == 401

        ok = client.post(
            "/chat",
            json={"texto": "oi Omega"},
            headers={"X-Omega-Token": "omega-dev-local"},
        )
        assert ok.status_code == 200
        body = ok.json()
        assert "resposta" in body

        tempo = client.get("/tempo")
        assert tempo.status_code == 200


def test_backup_endpoint():
    with TestClient(app) as client:
        headers = {"X-Omega-Token": "omega-dev-local"}
        r = client.post("/backups", headers=headers, params={"rotulo": "teste_api"})
        assert r.status_code == 200
        assert "id" in r.json()
