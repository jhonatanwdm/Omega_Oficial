import 'package:flutter/material.dart';

/// Tema Omega — atmosfera florestal-oceânica (evita clichês roxo/creme).
class OmegaTema {
  static const Color verdeProfundo = Color(0xFF1F6F5B);
  static const Color azulNoite = Color(0xFF0E2A3A);
  static const Color areiaQuente = Color(0xFFE6D3B3);
  static const Color cobre = Color(0xFFC9892D);
  static const Color gelo = Color(0xFFF3F7F5);

  static ThemeData claro() {
    final base = ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: ColorScheme.fromSeed(
        seedColor: verdeProfundo,
        brightness: Brightness.light,
        primary: verdeProfundo,
        secondary: cobre,
        surface: gelo,
      ),
      fontFamily: 'Segoe UI',
    );
    return base.copyWith(
      scaffoldBackgroundColor: gelo,
      textTheme: base.textTheme.copyWith(
        displayLarge: const TextStyle(
          fontSize: 56,
          fontWeight: FontWeight.w700,
          letterSpacing: -1.2,
          color: azulNoite,
        ),
        headlineMedium: const TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.w500,
          color: azulNoite,
        ),
        bodyLarge: const TextStyle(fontSize: 16, height: 1.4, color: azulNoite),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: verdeProfundo,
          foregroundColor: gelo,
          padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        ),
      ),
    );
  }
}
