import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:omega_cliente/estado/omega_estado.dart';
import 'package:omega_cliente/tema/omega_tema.dart';

class TelaInicio extends ConsumerStatefulWidget {
  const TelaInicio({super.key});

  @override
  ConsumerState<TelaInicio> createState() => _TelaInicioState();
}

class _TelaInicioState extends ConsumerState<TelaInicio> {
  final _ctrl = TextEditingController();
  bool _mostrarChat = false;

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  Color _corFase(OmegaFaseAnimacao fase) {
    switch (fase) {
      case OmegaFaseAnimacao.ouvindo:
        return const Color(0xFF2F9E7F);
      case OmegaFaseAnimacao.pensando:
        return OmegaTema.cobre;
      case OmegaFaseAnimacao.falando:
        return const Color(0xFF1D4E89);
      case OmegaFaseAnimacao.alerta:
        return const Color(0xFFA33B2B);
      case OmegaFaseAnimacao.idle:
        return OmegaTema.verdeProfundo;
    }
  }

  String _rotuloFase(OmegaFaseAnimacao fase) {
    switch (fase) {
      case OmegaFaseAnimacao.ouvindo:
        return 'ouvindo';
      case OmegaFaseAnimacao.pensando:
        return 'pensando';
      case OmegaFaseAnimacao.falando:
        return 'falando';
      case OmegaFaseAnimacao.alerta:
        return 'alerta';
      case OmegaFaseAnimacao.idle:
        return 'pronto';
    }
  }

  @override
  Widget build(BuildContext context) {
    final chat = ref.watch(omegaChatProvider);
    final theme = Theme.of(context);

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFF0E2A3A),
              Color(0xFF1F6F5B),
              Color(0xFFE6D3B3),
            ],
            stops: [0.0, 0.55, 1.0],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (!_mostrarChat) ...[
                  Text(
                    'Omega',
                    style: theme.textTheme.displayLarge?.copyWith(
                      color: OmegaTema.gelo,
                    ),
                  )
                      .animate()
                      .fadeIn(duration: 700.ms)
                      .slideY(begin: 0.15, end: 0),
                  const SizedBox(height: 8),
                  Text(
                    'Seu agente pessoal, sempre perto.',
                    style: theme.textTheme.headlineMedium?.copyWith(
                      color: OmegaTema.areiaQuente,
                    ),
                  ).animate().fadeIn(delay: 200.ms, duration: 700.ms),
                  const SizedBox(height: 36),
                  Center(child: _Orbe(cor: _corFase(chat.fase))),
                  const SizedBox(height: 28),
                  ElevatedButton(
                    onPressed: () => setState(() => _mostrarChat = true),
                    child: const Text('Conversar'),
                  ).animate().fadeIn(delay: 350.ms),
                ] else ...[
                  Row(
                    children: [
                      Text(
                        'Omega',
                        style: theme.textTheme.headlineMedium?.copyWith(
                          color: OmegaTema.gelo,
                          fontFamily: 'Segoe UI',
                          fontWeight: FontWeight.w700,
                          fontSize: 28,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Text(
                        _rotuloFase(chat.fase),
                        style: TextStyle(
                          color: OmegaTema.areiaQuente.withValues(alpha: 0.85),
                          fontSize: 12,
                          letterSpacing: 1.1,
                        ),
                      ),
                      const Spacer(),
                      IconButton(
                        tooltip: 'Voz',
                        onPressed: chat.carregando
                            ? null
                            : () => ref.read(omegaChatProvider.notifier).alternarGravacao(),
                        icon: Icon(
                          chat.gravando ? Icons.stop_circle_outlined : Icons.mic_none,
                          color: OmegaTema.gelo,
                        ),
                      ),
                      IconButton(
                        tooltip: 'Sincronizar',
                        onPressed: () => ref.read(omegaChatProvider.notifier).sincronizar(),
                        icon: const Icon(Icons.sync, color: OmegaTema.gelo),
                      ),
                    ],
                  ).animate().fadeIn(duration: 400.ms),
                  const SizedBox(height: 8),
                  Align(
                    alignment: Alignment.centerLeft,
                    child: SizedBox(
                      width: 56,
                      height: 56,
                      child: _Orbe(cor: _corFase(chat.fase), compacto: true),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Expanded(
                    child: ListView.builder(
                      itemCount: chat.mensagens.length,
                      itemBuilder: (context, i) {
                        final m = chat.mensagens[i];
                        final eu = m['papel'] == 'usuario';
                        return Align(
                          alignment: eu ? Alignment.centerRight : Alignment.centerLeft,
                          child: Container(
                            margin: const EdgeInsets.symmetric(vertical: 6),
                            padding: const EdgeInsets.all(12),
                            constraints: const BoxConstraints(maxWidth: 520),
                            decoration: BoxDecoration(
                              color: eu
                                  ? Colors.white.withValues(alpha: 0.16)
                                  : Colors.black.withValues(alpha: 0.22),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              m['conteudo'] ?? '',
                              style: const TextStyle(color: Colors.white, height: 1.35),
                            ),
                          ),
                        ).animate().fadeIn(duration: 280.ms).slideY(begin: 0.08, end: 0);
                      },
                    ),
                  ),
                  if (chat.erro != null)
                    Text(chat.erro!, style: const TextStyle(color: Color(0xFFFFD0C8))),
                  if (chat.statusSync != null)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 6),
                      child: Text(
                        chat.statusSync!,
                        style: TextStyle(color: OmegaTema.areiaQuente.withValues(alpha: 0.9)),
                      ),
                    ),
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _ctrl,
                          style: const TextStyle(color: Colors.white),
                          decoration: InputDecoration(
                            hintText: 'Fale com o Omega...',
                            hintStyle: TextStyle(color: Colors.white.withValues(alpha: 0.7)),
                            filled: true,
                            fillColor: Colors.black.withValues(alpha: 0.2),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(14),
                              borderSide: BorderSide.none,
                            ),
                          ),
                          onSubmitted: (_) => _enviar(),
                        ),
                      ),
                      const SizedBox(width: 10),
                      IconButton.filled(
                        onPressed: chat.carregando ? null : _enviar,
                        style: IconButton.styleFrom(backgroundColor: OmegaTema.verdeProfundo),
                        icon: chat.carregando
                            ? const SizedBox(
                                width: 18,
                                height: 18,
                                child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                              )
                            : const Icon(Icons.send),
                      ),
                    ],
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _enviar() {
    final texto = _ctrl.text;
    _ctrl.clear();
    ref.read(omegaChatProvider.notifier).enviar(texto);
  }
}

class _Orbe extends StatelessWidget {
  const _Orbe({required this.cor, this.compacto = false});

  final Color cor;
  final bool compacto;

  @override
  Widget build(BuildContext context) {
    final size = compacto ? 56.0 : 160.0;
    final icon = compacto ? 22.0 : 64.0;
    return AnimatedContainer(
      duration: const Duration(milliseconds: 450),
      width: size,
      height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: cor.withValues(alpha: 0.85),
        boxShadow: [
          BoxShadow(
            color: cor.withValues(alpha: 0.45),
            blurRadius: compacto ? 16 : 36,
            spreadRadius: compacto ? 2 : 6,
          ),
        ],
      ),
      child: Icon(Icons.graphic_eq, size: icon, color: Colors.white),
    )
        .animate(onPlay: (c) => c.repeat(reverse: true))
        .scale(
          begin: const Offset(0.96, 0.96),
          end: const Offset(1.04, 1.04),
          duration: 1600.ms,
        );
  }
}
