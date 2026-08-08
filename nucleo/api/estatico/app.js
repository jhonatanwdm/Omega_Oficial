(() => {
  const TOKEN = "omega-dev-local";
  const BASE = "";

  const el = {
    hero: document.getElementById("hero"),
    painel: document.getElementById("painelChat"),
    orbe: document.getElementById("orbe"),
    orbeMini: document.getElementById("orbeMini"),
    chipFase: document.getElementById("chipFase"),
    status: document.getElementById("statusHub"),
    statusChat: document.getElementById("statusChat"),
    mensagens: document.getElementById("mensagens"),
    form: document.getElementById("formChat"),
    entrada: document.getElementById("entrada"),
    btnIniciar: document.getElementById("btnIniciar"),
    btnVoz: document.getElementById("btnVoz"),
    btnSync: document.getElementById("btnSync"),
  };

  const rotulos = {
    idle: "pronto",
    ouvindo: "ouvindo",
    pensando: "pensando",
    falando: "falando",
    alerta: "alerta",
  };

  let conversaId = null;
  let ouvindo = false;
  let reconhecimento = null;

  function setFase(fase) {
    const f = fase || "idle";
    for (const node of [el.orbe, el.orbeMini]) {
      if (!node) continue;
      node.classList.remove("idle", "ouvindo", "pensando", "falando", "alerta");
      node.classList.add(f);
    }
    if (el.chipFase) el.chipFase.textContent = rotulos[f] || f;
  }

  function bolha(papel, texto) {
    const wrap = document.createElement("article");
    wrap.className = `msg ${papel === "usuario" ? "usuario" : "omega"}`;

    const quem = document.createElement("span");
    quem.className = "papel";
    quem.textContent = papel === "usuario" ? "Você" : "Omega";

    const corpo = document.createElement("p");
    corpo.className = "texto";
    corpo.textContent = texto;

    wrap.append(quem, corpo);
    el.mensagens.appendChild(wrap);
    el.mensagens.scrollTop = el.mensagens.scrollHeight;
  }

  function setStatus(texto) {
    if (el.status) el.status.textContent = texto;
    if (el.statusChat) {
      el.statusChat.hidden = false;
      el.statusChat.textContent = texto;
    }
  }

  async function api(path, opts = {}) {
    const headers = Object.assign(
      { "X-Omega-Token": TOKEN, "Content-Type": "application/json" },
      opts.headers || {}
    );
    const r = await fetch(BASE + path, { ...opts, headers });
    if (!r.ok) {
      const t = await r.text();
      throw new Error(t || `HTTP ${r.status}`);
    }
    return r.json();
  }

  async function checarHub() {
    try {
      const s = await fetch(BASE + "/saude").then((r) => r.json());
      setStatus(s.ok ? `Hub online · v${s.versao || "?"}` : "Hub com problemas");
      setFase("idle");
    } catch {
      setStatus("Hub offline — inicie o Omega");
      setFase("alerta");
    }
  }

  function falar(texto) {
    if (!window.speechSynthesis || !texto) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(texto);
    u.lang = "pt-BR";
    u.rate = 1.02;
    setFase("falando");
    u.onend = () => setFase("idle");
    u.onerror = () => setFase("idle");
    window.speechSynthesis.speak(u);
  }

  async function enviar(texto) {
    const t = (texto || "").trim();
    if (!t) return;
    bolha("usuario", t);
    el.entrada.value = "";
    setFase("pensando");
    try {
      const r = await api("/chat", {
        method: "POST",
        body: JSON.stringify({
          texto: t,
          conversa_id: conversaId,
          plataforma: "web",
          modo: "texto",
          confirmado: false,
        }),
      });
      conversaId = r.conversa_id || conversaId;
      const resposta = r.resposta || "(sem resposta)";
      bolha("omega", resposta);
      falar(resposta);
    } catch (e) {
      setFase("alerta");
      bolha("omega", "Não consegui falar com o hub: " + e.message);
    }
  }

  function iniciarVoz() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      bolha("omega", "Reconhecimento de voz não disponível neste navegador.");
      setFase("alerta");
      return;
    }
    if (!reconhecimento) {
      reconhecimento = new SR();
      reconhecimento.lang = "pt-BR";
      reconhecimento.interimResults = false;
      reconhecimento.continuous = false;
      reconhecimento.onstart = () => {
        ouvindo = true;
        el.btnVoz.classList.add("ativo");
        setFase("ouvindo");
      };
      reconhecimento.onend = () => {
        ouvindo = false;
        el.btnVoz.classList.remove("ativo");
        if (el.orbeMini?.classList.contains("ouvindo") || el.orbe?.classList.contains("ouvindo")) {
          setFase("idle");
        }
      };
      reconhecimento.onerror = () => {
        ouvindo = false;
        el.btnVoz.classList.remove("ativo");
        setFase("alerta");
      };
      reconhecimento.onresult = (ev) => {
        const texto = ev.results?.[0]?.[0]?.transcript || "";
        if (texto) enviar(texto);
      };
    }
    if (ouvindo) {
      reconhecimento.stop();
      return;
    }
    reconhecimento.start();
  }

  async function sincronizar() {
    setFase("pensando");
    el.btnSync.classList.add("ativo");
    try {
      const entidades = ["mensagens", "conhecimento", "agenda"];
      for (const entidade of entidades) {
        await api("/sync/pull", {
          method: "POST",
          body: JSON.stringify({ entidade, desde_versao: 0 }),
        });
      }
      const tempo = await fetch(BASE + "/tempo").then((r) => r.json());
      bolha("omega", `Sincronizado. Relógio hub: ${tempo.local || tempo.utc || "ok"}`);
      setFase("idle");
    } catch (e) {
      setFase("alerta");
      bolha("omega", "Falha no sync: " + e.message);
    } finally {
      el.btnSync.classList.remove("ativo");
    }
  }

  el.btnIniciar.addEventListener("click", () => {
    el.hero.classList.add("oculto");
    el.painel.classList.remove("oculto");
    if (el.statusChat && el.status) {
      el.statusChat.hidden = false;
      el.statusChat.textContent = el.status.textContent;
    }
    el.entrada.focus();
    setFase("idle");
  });

  el.form.addEventListener("submit", (ev) => {
    ev.preventDefault();
    enviar(el.entrada.value);
  });

  el.btnVoz.addEventListener("click", iniciarVoz);
  el.btnSync.addEventListener("click", sincronizar);

  setFase("idle");
  checarHub();
  setInterval(checarHub, 15000);
})();
