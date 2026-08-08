# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

raiz = Path(SPECPATH)

hidden = []
for pacote in (
    "nucleo",
    "sub_agentes",
    "uvicorn",
    "starlette",
    "fastapi",
    "pydantic",
    "sqlalchemy",
    "sqlmodel",
    "aiosqlite",
    "httpx",
    "yaml",
    "structlog",
    "pendulum",
    "multipart",
    "anyio",
):
    try:
        hidden += collect_submodules(pacote)
    except Exception:
        pass

a = Analysis(
    [str(raiz / "scripts" / "omega_hub_entry.py")],
    pathex=[str(raiz)],
    binaries=[],
    datas=[
        (str(raiz / "configs"), "configs"),
        (str(raiz / "dados" / "versao.json"), "dados"),
        (str(raiz / "contratos"), "contratos"),
        (str(raiz / "nucleo" / "api" / "estatico"), "nucleo/api/estatico"),
    ],
    hiddenimports=hidden
    + [
        "nucleo.api.principal",
        "nucleo.api.esquemas",
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.lifespan",
        "uvicorn.lifespan.on",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "torch",
        "tensorflow",
        "faster_whisper",
        "sentence_transformers",
        "qdrant_client",
        "matplotlib",
        "tkinter",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

# Um único arquivo .exe
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Omega",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
