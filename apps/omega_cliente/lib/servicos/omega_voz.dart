/// Hooks de captura/reprodução de voz.
///
/// Sem plugins nativos (record/just_audio) para o build Windows funcionar
/// sem Developer Mode / symlinks. A UI web do hub cobre Web Speech;
/// aqui o stub permite plugar gravadores nativos depois.
class OmegaVoz {
  bool _gravando = false;
  String? _ultimaNota;

  bool get gravando => _gravando;

  Future<bool> microfoneDisponivel() async => false;

  Future<String?> iniciarGravacao() async {
    _gravando = true;
    _ultimaNota = 'voz-hook-${DateTime.now().millisecondsSinceEpoch}';
    return _ultimaNota;
  }

  Future<String?> pararGravacao() async {
    _gravando = false;
    return _ultimaNota;
  }

  Future<void> reproduzirArquivo(String caminho) async {
    // Hook: integrar just_audio quando Developer Mode estiver ativo.
  }

  Future<void> dispose() async {}
}
