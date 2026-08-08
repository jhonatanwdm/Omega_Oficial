import 'package:omega_cliente/servicos/omega_api.dart';

/// Sincronização simples cliente ← hub (cursor por entidade).
class OmegaSync {
  OmegaSync(this.api);

  final OmegaApi api;
  final Map<String, int> _cursores = {
    'mensagens': 0,
    'conhecimento': 0,
    'agenda': 0,
  };

  Future<Map<String, dynamic>> puxarTudo() async {
    final out = <String, dynamic>{};
    for (final entidade in _cursores.keys) {
      final r = await api.syncPull(entidade, _cursores[entidade] ?? 0);
      _cursores[entidade] = (r['cursor'] as int?) ?? _cursores[entidade]!;
      out[entidade] = r;
    }
    return out;
  }
}
