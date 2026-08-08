import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:omega_cliente/dados/omega_db.dart';
import 'package:omega_cliente/servicos/omega_api.dart';
import 'package:omega_cliente/servicos/omega_sync.dart';
import 'package:omega_cliente/servicos/omega_voz.dart';

enum OmegaFaseAnimacao { idle, ouvindo, pensando, falando, alerta }

class OmegaChatState {
  const OmegaChatState({
    this.conversaId,
    this.mensagens = const [],
    this.fase = OmegaFaseAnimacao.idle,
    this.carregando = false,
    this.gravando = false,
    this.erro,
    this.statusSync,
  });

  final String? conversaId;
  final List<Map<String, String>> mensagens;
  final OmegaFaseAnimacao fase;
  final bool carregando;
  final bool gravando;
  final String? erro;
  final String? statusSync;

  OmegaChatState copyWith({
    String? conversaId,
    List<Map<String, String>>? mensagens,
    OmegaFaseAnimacao? fase,
    bool? carregando,
    bool? gravando,
    String? erro,
    String? statusSync,
    bool limparErro = false,
    bool limparSync = false,
  }) {
    return OmegaChatState(
      conversaId: conversaId ?? this.conversaId,
      mensagens: mensagens ?? this.mensagens,
      fase: fase ?? this.fase,
      carregando: carregando ?? this.carregando,
      gravando: gravando ?? this.gravando,
      erro: limparErro ? null : (erro ?? this.erro),
      statusSync: limparSync ? null : (statusSync ?? this.statusSync),
    );
  }
}

final omegaApiProvider = Provider<OmegaApi>((ref) => OmegaApi());

final omegaDbProvider = Provider<OmegaDb>((ref) {
  final db = OmegaDb();
  ref.onDispose(db.close);
  return db;
});

final omegaSyncProvider = Provider<OmegaSync>((ref) {
  return OmegaSync(ref.watch(omegaApiProvider), ref.watch(omegaDbProvider));
});

final omegaVozProvider = Provider<OmegaVoz>((ref) {
  final voz = OmegaVoz();
  ref.onDispose(voz.dispose);
  return voz;
});

class OmegaChatNotifier extends StateNotifier<OmegaChatState> {
  OmegaChatNotifier(this._api, this._db, this._sync, this._voz)
      : super(const OmegaChatState());

  final OmegaApi _api;
  final OmegaDb _db;
  final OmegaSync _sync;
  final OmegaVoz _voz;

  Future<void> enviar(String texto, {String modo = 'texto'}) async {
    if (texto.trim().isEmpty) return;
    final msgs = [
      ...state.mensagens,
      {'papel': 'usuario', 'conteudo': texto},
    ];
    state = state.copyWith(
      mensagens: msgs,
      carregando: true,
      fase: OmegaFaseAnimacao.pensando,
      limparErro: true,
    );
    try {
      final r = await _api.chat(
        texto: texto,
        conversaId: state.conversaId,
        plataforma: 'desktop',
        modo: modo,
      );
      final resposta = (r['resposta'] ?? '') as String;
      final conversaId = (r['conversa_id'] as String?) ?? state.conversaId ?? 'local';
      final agora = DateTime.now().millisecondsSinceEpoch;
      await _db.salvarMensagem(
        id: 'u-$agora',
        conversaId: conversaId,
        papel: 'usuario',
        conteudo: texto,
      );
      await _db.salvarMensagem(
        id: 'o-$agora',
        conversaId: conversaId,
        papel: 'omega',
        conteudo: resposta,
      );
      state = state.copyWith(
        conversaId: conversaId,
        mensagens: [
          ...msgs,
          {'papel': 'omega', 'conteudo': resposta},
        ],
        carregando: false,
        fase: OmegaFaseAnimacao.falando,
      );
      await Future<void>.delayed(const Duration(milliseconds: 800));
      state = state.copyWith(fase: OmegaFaseAnimacao.idle);
    } catch (e) {
      state = state.copyWith(
        carregando: false,
        fase: OmegaFaseAnimacao.alerta,
        erro: e.toString(),
      );
    }
  }

  Future<void> sincronizar() async {
    state = state.copyWith(fase: OmegaFaseAnimacao.pensando, limparSync: true);
    try {
      await _sync.puxarTudo();
      final tempo = await _api.tempo();
      state = state.copyWith(
        fase: OmegaFaseAnimacao.idle,
        statusSync: 'Sync ok · ${tempo['local'] ?? tempo['utc'] ?? 'hub'}',
      );
    } catch (e) {
      state = state.copyWith(
        fase: OmegaFaseAnimacao.alerta,
        statusSync: 'Sync falhou: $e',
      );
    }
  }

  Future<void> alternarGravacao() async {
    if (state.gravando) {
      await _voz.pararGravacao();
      state = state.copyWith(gravando: false, fase: OmegaFaseAnimacao.idle);
      state = state.copyWith(
        erro:
            'Voz nativa em stub neste build. Use a UI web do hub (Web Speech) em http://127.0.0.1:8741/',
        fase: OmegaFaseAnimacao.alerta,
      );
      return;
    }
    await _voz.iniciarGravacao();
    state = state.copyWith(
      gravando: true,
      fase: OmegaFaseAnimacao.ouvindo,
      limparErro: true,
    );
  }
}

final omegaChatProvider =
    StateNotifierProvider<OmegaChatNotifier, OmegaChatState>(
  (ref) => OmegaChatNotifier(
    ref.watch(omegaApiProvider),
    ref.watch(omegaDbProvider),
    ref.watch(omegaSyncProvider),
    ref.watch(omegaVozProvider),
  ),
);
