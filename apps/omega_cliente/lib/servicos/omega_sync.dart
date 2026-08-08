import 'package:omega_cliente/dados/omega_db.dart';
import 'package:omega_cliente/servicos/omega_api.dart';

/// Sincronização cliente ← hub com cursores persistidos no Drift.
class OmegaSync {
  OmegaSync(this.api, this.db);

  final OmegaApi api;
  final OmegaDb db;

  static const entidades = ['mensagens', 'conhecimento', 'agenda'];

  Future<Map<String, dynamic>> puxarTudo() async {
    final out = <String, dynamic>{};
    for (final entidade in entidades) {
      final desde = await db.cursorDe(entidade);
      final r = await api.syncPull(entidade, desde);
      final cursor = (r['cursor'] as num?)?.toInt() ?? desde;
      await db.salvarCursor(entidade, cursor);
      out[entidade] = r;
    }
    return out;
  }
}
