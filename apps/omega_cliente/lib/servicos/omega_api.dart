import 'package:dio/dio.dart';

class OmegaApi {
  OmegaApi({
    this.baseUrl = 'http://127.0.0.1:8741',
    this.token = 'omega-dev-local',
  }) : _dio = Dio(BaseOptions(
          baseUrl: baseUrl,
          headers: {'X-Omega-Token': token},
          connectTimeout: const Duration(seconds: 10),
        ));

  final String baseUrl;
  final String token;
  final Dio _dio;

  Future<Map<String, dynamic>> saude() async {
    final r = await _dio.get('/saude');
    return Map<String, dynamic>.from(r.data as Map);
  }

  Future<Map<String, dynamic>> chat({
    required String texto,
    String? conversaId,
    String plataforma = 'desktop',
    bool confirmado = false,
    String modo = 'texto',
  }) async {
    final r = await _dio.post('/chat', data: {
      'texto': texto,
      'conversa_id': conversaId,
      'plataforma': plataforma,
      'confirmado': confirmado,
      'modo': modo,
    });
    return Map<String, dynamic>.from(r.data as Map);
  }

  Future<Map<String, dynamic>> syncPull(String entidade, int desde) async {
    final r = await _dio.post('/sync/pull', data: {
      'entidade': entidade,
      'desde_versao': desde,
    });
    return Map<String, dynamic>.from(r.data as Map);
  }

  Future<Map<String, dynamic>> tempo() async {
    final r = await _dio.get('/tempo');
    return Map<String, dynamic>.from(r.data as Map);
  }
}
