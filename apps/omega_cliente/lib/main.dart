import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:omega_cliente/telas/tela_inicio.dart';
import 'package:omega_cliente/tema/omega_tema.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ProviderScope(child: OmegaApp()));
}

class OmegaApp extends StatelessWidget {
  const OmegaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Omega',
      debugShowCheckedModeBanner: false,
      theme: OmegaTema.claro(),
      locale: const Locale('pt'),
      supportedLocales: const [
        Locale('pt'),
        Locale('en'),
        Locale('es'),
      ],
      home: const TelaInicio(),
    );
  }
}
