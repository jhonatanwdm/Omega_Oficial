import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:omega_cliente/servicos/omega_api.dart';

enum OmegaFaseAnimacao { idle, ouvindo, pensando, falando, alerta }

class OmegaChatState {
  const OmegaChatState({
    this.conversaId,
    this.mensagens = const [],
    this.fase = OmegaFaseAnimacao.idle,
    this.carregando = false,
    this.erro,
  });

  final String? conversaId;
  final List<Map<String, String>> mensagens;
  final OmegaFaseAnimacao fase;
  final bool carregando;
  final String? erro;

  OmegaChatState copyWith({
    String? conversaId,
    List<Map<String, String>>? mensagens,
    OmegaFaseAnimacao? fase,
    bool? carregando,
    String? erro,
  }) {
    return OmegaChatState(
      conversaId: conversaId ?? this.conversaId,
      mensagens: mensagens ?? this.mensagens,
      fase: fase ?? this.fase,
      carregando: carregando ?? this.carregando,
      erro: erro,
    );
  }
}

final omegaApiProvider = Provider<OmegaApi>((ref) => OmegaApi());

class OmegaChatNotifier extends StateNotifier<OmegaChatState> {
  OmegaChatNotifier(this._api) : super(const OmegaChatState());

  final OmegaApi _api;

  Future<void> enviar(String texto) async {
    if (texto.trim().isEmpty) return;
    final msgs = [
      ...state.mensagens,
      {'papel': 'usuario', 'conteudo': texto},
    ];
    state = state.copyWith(
      mensagens: msgs,
      carregando: true,
      fase: OmegaFaseAnimacao.pensando,
      erro: null,
    );
    try {
      final r = await _api.chat(
        texto: texto,
        conversaId: state.conversaId,
        plataforma: 'desktop',
      );
      final resposta = (r['resposta'] ?? '') as String;
      state = state.copyWith(
        conversaId: r['conversa_id'] as String?,
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
}

final omegaChatProvider =
    StateNotifierProvider<OmegaChatNotifier, OmegaChatState>(
  (ref) => OmegaChatNotifier(ref.watch(omegaApiProvider)),
);
