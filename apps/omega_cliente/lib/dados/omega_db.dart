import 'dart:io';

import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path/path.dart' as p;

part 'omega_db.g.dart';

@DataClassName('MensagemLocal')
class MensagensLocais extends Table {
  TextColumn get id => text()();
  TextColumn get conversaId => text()();
  TextColumn get papel => text()();
  TextColumn get conteudo => text()();
  DateTimeColumn get criadoEm => dateTime().withDefault(currentDateAndTime)();
  IntColumn get versaoSync => integer().withDefault(const Constant(0))();

  @override
  Set<Column> get primaryKey => {id};
}

@DataClassName('CursorSync')
class CursoresSync extends Table {
  TextColumn get entidade => text()();
  IntColumn get cursor => integer().withDefault(const Constant(0))();

  @override
  Set<Column> get primaryKey => {entidade};
}

@DriftDatabase(tables: [MensagensLocais, CursoresSync])
class OmegaDb extends _$OmegaDb {
  OmegaDb() : super(_abrirConexao());

  OmegaDb.paraTeste(super.e);

  @override
  int get schemaVersion => 1;

  Future<void> salvarMensagem({
    required String id,
    required String conversaId,
    required String papel,
    required String conteudo,
    int versaoSync = 0,
  }) {
    return into(mensagensLocais).insertOnConflictUpdate(
      MensagensLocaisCompanion.insert(
        id: id,
        conversaId: conversaId,
        papel: papel,
        conteudo: conteudo,
        versaoSync: Value(versaoSync),
      ),
    );
  }

  Future<List<MensagemLocal>> listarMensagens(String conversaId) {
    return (select(mensagensLocais)
          ..where((t) => t.conversaId.equals(conversaId))
          ..orderBy([(t) => OrderingTerm.asc(t.criadoEm)]))
        .get();
  }

  Future<int> cursorDe(String entidade) async {
    final row = await (select(cursoresSync)..where((t) => t.entidade.equals(entidade)))
        .getSingleOrNull();
    return row?.cursor ?? 0;
  }

  Future<void> salvarCursor(String entidade, int cursor) {
    return into(cursoresSync).insertOnConflictUpdate(
      CursoresSyncCompanion.insert(entidade: entidade, cursor: Value(cursor)),
    );
  }
}

Directory _dirDados() {
  final appData = Platform.environment['APPDATA'] ??
      Platform.environment['LOCALAPPDATA'] ??
      Directory.systemTemp.path;
  final dir = Directory(p.join(appData, 'Omega', 'cliente'));
  if (!dir.existsSync()) {
    dir.createSync(recursive: true);
  }
  return dir;
}

LazyDatabase _abrirConexao() {
  return LazyDatabase(() async {
    final arquivo = File(p.join(_dirDados().path, 'omega_local.sqlite'));
    return NativeDatabase.createInBackground(arquivo);
  });
}
