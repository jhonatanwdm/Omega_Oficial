import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:omega_cliente/main.dart';

void main() {
  testWidgets('Omega mostra marca na home', (tester) async {
    await tester.pumpWidget(const ProviderScope(child: OmegaApp()));
    expect(find.text('Omega'), findsOneWidget);
    expect(find.text('Conversar'), findsOneWidget);
  });
}
