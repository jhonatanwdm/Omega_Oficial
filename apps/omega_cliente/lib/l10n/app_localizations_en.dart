// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appNome => 'Omega';

  @override
  String get subtitulo => 'Your personal agent, always near.';

  @override
  String get ctaConversar => 'Talk';

  @override
  String get placeholder => 'Talk to Omega...';

  @override
  String get enviando => 'Thinking...';

  @override
  String get voz => 'Voice';

  @override
  String get texto => 'Text';
}
