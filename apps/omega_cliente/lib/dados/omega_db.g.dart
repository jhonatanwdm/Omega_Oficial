// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'omega_db.dart';

// ignore_for_file: type=lint
class $MensagensLocaisTable extends MensagensLocais
    with TableInfo<$MensagensLocaisTable, MensagemLocal> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $MensagensLocaisTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _idMeta = const VerificationMeta('id');
  @override
  late final GeneratedColumn<String> id = GeneratedColumn<String>(
      'id', aliasedName, false,
      type: DriftSqlType.string, requiredDuringInsert: true);
  static const VerificationMeta _conversaIdMeta =
      const VerificationMeta('conversaId');
  @override
  late final GeneratedColumn<String> conversaId = GeneratedColumn<String>(
      'conversa_id', aliasedName, false,
      type: DriftSqlType.string, requiredDuringInsert: true);
  static const VerificationMeta _papelMeta = const VerificationMeta('papel');
  @override
  late final GeneratedColumn<String> papel = GeneratedColumn<String>(
      'papel', aliasedName, false,
      type: DriftSqlType.string, requiredDuringInsert: true);
  static const VerificationMeta _conteudoMeta =
      const VerificationMeta('conteudo');
  @override
  late final GeneratedColumn<String> conteudo = GeneratedColumn<String>(
      'conteudo', aliasedName, false,
      type: DriftSqlType.string, requiredDuringInsert: true);
  static const VerificationMeta _criadoEmMeta =
      const VerificationMeta('criadoEm');
  @override
  late final GeneratedColumn<DateTime> criadoEm = GeneratedColumn<DateTime>(
      'criado_em', aliasedName, false,
      type: DriftSqlType.dateTime,
      requiredDuringInsert: false,
      defaultValue: currentDateAndTime);
  static const VerificationMeta _versaoSyncMeta =
      const VerificationMeta('versaoSync');
  @override
  late final GeneratedColumn<int> versaoSync = GeneratedColumn<int>(
      'versao_sync', aliasedName, false,
      type: DriftSqlType.int,
      requiredDuringInsert: false,
      defaultValue: const Constant(0));
  @override
  List<GeneratedColumn> get $columns =>
      [id, conversaId, papel, conteudo, criadoEm, versaoSync];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'mensagens_locais';
  @override
  VerificationContext validateIntegrity(Insertable<MensagemLocal> instance,
      {bool isInserting = false}) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('id')) {
      context.handle(_idMeta, id.isAcceptableOrUnknown(data['id']!, _idMeta));
    } else if (isInserting) {
      context.missing(_idMeta);
    }
    if (data.containsKey('conversa_id')) {
      context.handle(
          _conversaIdMeta,
          conversaId.isAcceptableOrUnknown(
              data['conversa_id']!, _conversaIdMeta));
    } else if (isInserting) {
      context.missing(_conversaIdMeta);
    }
    if (data.containsKey('papel')) {
      context.handle(
          _papelMeta, papel.isAcceptableOrUnknown(data['papel']!, _papelMeta));
    } else if (isInserting) {
      context.missing(_papelMeta);
    }
    if (data.containsKey('conteudo')) {
      context.handle(_conteudoMeta,
          conteudo.isAcceptableOrUnknown(data['conteudo']!, _conteudoMeta));
    } else if (isInserting) {
      context.missing(_conteudoMeta);
    }
    if (data.containsKey('criado_em')) {
      context.handle(_criadoEmMeta,
          criadoEm.isAcceptableOrUnknown(data['criado_em']!, _criadoEmMeta));
    }
    if (data.containsKey('versao_sync')) {
      context.handle(
          _versaoSyncMeta,
          versaoSync.isAcceptableOrUnknown(
              data['versao_sync']!, _versaoSyncMeta));
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {id};
  @override
  MensagemLocal map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return MensagemLocal(
      id: attachedDatabase.typeMapping
          .read(DriftSqlType.string, data['${effectivePrefix}id'])!,
      conversaId: attachedDatabase.typeMapping
          .read(DriftSqlType.string, data['${effectivePrefix}conversa_id'])!,
      papel: attachedDatabase.typeMapping
          .read(DriftSqlType.string, data['${effectivePrefix}papel'])!,
      conteudo: attachedDatabase.typeMapping
          .read(DriftSqlType.string, data['${effectivePrefix}conteudo'])!,
      criadoEm: attachedDatabase.typeMapping
          .read(DriftSqlType.dateTime, data['${effectivePrefix}criado_em'])!,
      versaoSync: attachedDatabase.typeMapping
          .read(DriftSqlType.int, data['${effectivePrefix}versao_sync'])!,
    );
  }

  @override
  $MensagensLocaisTable createAlias(String alias) {
    return $MensagensLocaisTable(attachedDatabase, alias);
  }
}

class MensagemLocal extends DataClass implements Insertable<MensagemLocal> {
  final String id;
  final String conversaId;
  final String papel;
  final String conteudo;
  final DateTime criadoEm;
  final int versaoSync;
  const MensagemLocal(
      {required this.id,
      required this.conversaId,
      required this.papel,
      required this.conteudo,
      required this.criadoEm,
      required this.versaoSync});
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['id'] = Variable<String>(id);
    map['conversa_id'] = Variable<String>(conversaId);
    map['papel'] = Variable<String>(papel);
    map['conteudo'] = Variable<String>(conteudo);
    map['criado_em'] = Variable<DateTime>(criadoEm);
    map['versao_sync'] = Variable<int>(versaoSync);
    return map;
  }

  MensagensLocaisCompanion toCompanion(bool nullToAbsent) {
    return MensagensLocaisCompanion(
      id: Value(id),
      conversaId: Value(conversaId),
      papel: Value(papel),
      conteudo: Value(conteudo),
      criadoEm: Value(criadoEm),
      versaoSync: Value(versaoSync),
    );
  }

  factory MensagemLocal.fromJson(Map<String, dynamic> json,
      {ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return MensagemLocal(
      id: serializer.fromJson<String>(json['id']),
      conversaId: serializer.fromJson<String>(json['conversaId']),
      papel: serializer.fromJson<String>(json['papel']),
      conteudo: serializer.fromJson<String>(json['conteudo']),
      criadoEm: serializer.fromJson<DateTime>(json['criadoEm']),
      versaoSync: serializer.fromJson<int>(json['versaoSync']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'id': serializer.toJson<String>(id),
      'conversaId': serializer.toJson<String>(conversaId),
      'papel': serializer.toJson<String>(papel),
      'conteudo': serializer.toJson<String>(conteudo),
      'criadoEm': serializer.toJson<DateTime>(criadoEm),
      'versaoSync': serializer.toJson<int>(versaoSync),
    };
  }

  MensagemLocal copyWith(
          {String? id,
          String? conversaId,
          String? papel,
          String? conteudo,
          DateTime? criadoEm,
          int? versaoSync}) =>
      MensagemLocal(
        id: id ?? this.id,
        conversaId: conversaId ?? this.conversaId,
        papel: papel ?? this.papel,
        conteudo: conteudo ?? this.conteudo,
        criadoEm: criadoEm ?? this.criadoEm,
        versaoSync: versaoSync ?? this.versaoSync,
      );
  MensagemLocal copyWithCompanion(MensagensLocaisCompanion data) {
    return MensagemLocal(
      id: data.id.present ? data.id.value : this.id,
      conversaId:
          data.conversaId.present ? data.conversaId.value : this.conversaId,
      papel: data.papel.present ? data.papel.value : this.papel,
      conteudo: data.conteudo.present ? data.conteudo.value : this.conteudo,
      criadoEm: data.criadoEm.present ? data.criadoEm.value : this.criadoEm,
      versaoSync:
          data.versaoSync.present ? data.versaoSync.value : this.versaoSync,
    );
  }

  @override
  String toString() {
    return (StringBuffer('MensagemLocal(')
          ..write('id: $id, ')
          ..write('conversaId: $conversaId, ')
          ..write('papel: $papel, ')
          ..write('conteudo: $conteudo, ')
          ..write('criadoEm: $criadoEm, ')
          ..write('versaoSync: $versaoSync')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode =>
      Object.hash(id, conversaId, papel, conteudo, criadoEm, versaoSync);
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is MensagemLocal &&
          other.id == this.id &&
          other.conversaId == this.conversaId &&
          other.papel == this.papel &&
          other.conteudo == this.conteudo &&
          other.criadoEm == this.criadoEm &&
          other.versaoSync == this.versaoSync);
}

class MensagensLocaisCompanion extends UpdateCompanion<MensagemLocal> {
  final Value<String> id;
  final Value<String> conversaId;
  final Value<String> papel;
  final Value<String> conteudo;
  final Value<DateTime> criadoEm;
  final Value<int> versaoSync;
  final Value<int> rowid;
  const MensagensLocaisCompanion({
    this.id = const Value.absent(),
    this.conversaId = const Value.absent(),
    this.papel = const Value.absent(),
    this.conteudo = const Value.absent(),
    this.criadoEm = const Value.absent(),
    this.versaoSync = const Value.absent(),
    this.rowid = const Value.absent(),
  });
  MensagensLocaisCompanion.insert({
    required String id,
    required String conversaId,
    required String papel,
    required String conteudo,
    this.criadoEm = const Value.absent(),
    this.versaoSync = const Value.absent(),
    this.rowid = const Value.absent(),
  })  : id = Value(id),
        conversaId = Value(conversaId),
        papel = Value(papel),
        conteudo = Value(conteudo);
  static Insertable<MensagemLocal> custom({
    Expression<String>? id,
    Expression<String>? conversaId,
    Expression<String>? papel,
    Expression<String>? conteudo,
    Expression<DateTime>? criadoEm,
    Expression<int>? versaoSync,
    Expression<int>? rowid,
  }) {
    return RawValuesInsertable({
      if (id != null) 'id': id,
      if (conversaId != null) 'conversa_id': conversaId,
      if (papel != null) 'papel': papel,
      if (conteudo != null) 'conteudo': conteudo,
      if (criadoEm != null) 'criado_em': criadoEm,
      if (versaoSync != null) 'versao_sync': versaoSync,
      if (rowid != null) 'rowid': rowid,
    });
  }

  MensagensLocaisCompanion copyWith(
      {Value<String>? id,
      Value<String>? conversaId,
      Value<String>? papel,
      Value<String>? conteudo,
      Value<DateTime>? criadoEm,
      Value<int>? versaoSync,
      Value<int>? rowid}) {
    return MensagensLocaisCompanion(
      id: id ?? this.id,
      conversaId: conversaId ?? this.conversaId,
      papel: papel ?? this.papel,
      conteudo: conteudo ?? this.conteudo,
      criadoEm: criadoEm ?? this.criadoEm,
      versaoSync: versaoSync ?? this.versaoSync,
      rowid: rowid ?? this.rowid,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (id.present) {
      map['id'] = Variable<String>(id.value);
    }
    if (conversaId.present) {
      map['conversa_id'] = Variable<String>(conversaId.value);
    }
    if (papel.present) {
      map['papel'] = Variable<String>(papel.value);
    }
    if (conteudo.present) {
      map['conteudo'] = Variable<String>(conteudo.value);
    }
    if (criadoEm.present) {
      map['criado_em'] = Variable<DateTime>(criadoEm.value);
    }
    if (versaoSync.present) {
      map['versao_sync'] = Variable<int>(versaoSync.value);
    }
    if (rowid.present) {
      map['rowid'] = Variable<int>(rowid.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('MensagensLocaisCompanion(')
          ..write('id: $id, ')
          ..write('conversaId: $conversaId, ')
          ..write('papel: $papel, ')
          ..write('conteudo: $conteudo, ')
          ..write('criadoEm: $criadoEm, ')
          ..write('versaoSync: $versaoSync, ')
          ..write('rowid: $rowid')
          ..write(')'))
        .toString();
  }
}

class $CursoresSyncTable extends CursoresSync
    with TableInfo<$CursoresSyncTable, CursorSync> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $CursoresSyncTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _entidadeMeta =
      const VerificationMeta('entidade');
  @override
  late final GeneratedColumn<String> entidade = GeneratedColumn<String>(
      'entidade', aliasedName, false,
      type: DriftSqlType.string, requiredDuringInsert: true);
  static const VerificationMeta _cursorMeta = const VerificationMeta('cursor');
  @override
  late final GeneratedColumn<int> cursor = GeneratedColumn<int>(
      'cursor', aliasedName, false,
      type: DriftSqlType.int,
      requiredDuringInsert: false,
      defaultValue: const Constant(0));
  @override
  List<GeneratedColumn> get $columns => [entidade, cursor];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'cursores_sync';
  @override
  VerificationContext validateIntegrity(Insertable<CursorSync> instance,
      {bool isInserting = false}) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('entidade')) {
      context.handle(_entidadeMeta,
          entidade.isAcceptableOrUnknown(data['entidade']!, _entidadeMeta));
    } else if (isInserting) {
      context.missing(_entidadeMeta);
    }
    if (data.containsKey('cursor')) {
      context.handle(_cursorMeta,
          cursor.isAcceptableOrUnknown(data['cursor']!, _cursorMeta));
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {entidade};
  @override
  CursorSync map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return CursorSync(
      entidade: attachedDatabase.typeMapping
          .read(DriftSqlType.string, data['${effectivePrefix}entidade'])!,
      cursor: attachedDatabase.typeMapping
          .read(DriftSqlType.int, data['${effectivePrefix}cursor'])!,
    );
  }

  @override
  $CursoresSyncTable createAlias(String alias) {
    return $CursoresSyncTable(attachedDatabase, alias);
  }
}

class CursorSync extends DataClass implements Insertable<CursorSync> {
  final String entidade;
  final int cursor;
  const CursorSync({required this.entidade, required this.cursor});
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['entidade'] = Variable<String>(entidade);
    map['cursor'] = Variable<int>(cursor);
    return map;
  }

  CursoresSyncCompanion toCompanion(bool nullToAbsent) {
    return CursoresSyncCompanion(
      entidade: Value(entidade),
      cursor: Value(cursor),
    );
  }

  factory CursorSync.fromJson(Map<String, dynamic> json,
      {ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return CursorSync(
      entidade: serializer.fromJson<String>(json['entidade']),
      cursor: serializer.fromJson<int>(json['cursor']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'entidade': serializer.toJson<String>(entidade),
      'cursor': serializer.toJson<int>(cursor),
    };
  }

  CursorSync copyWith({String? entidade, int? cursor}) => CursorSync(
        entidade: entidade ?? this.entidade,
        cursor: cursor ?? this.cursor,
      );
  CursorSync copyWithCompanion(CursoresSyncCompanion data) {
    return CursorSync(
      entidade: data.entidade.present ? data.entidade.value : this.entidade,
      cursor: data.cursor.present ? data.cursor.value : this.cursor,
    );
  }

  @override
  String toString() {
    return (StringBuffer('CursorSync(')
          ..write('entidade: $entidade, ')
          ..write('cursor: $cursor')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode => Object.hash(entidade, cursor);
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is CursorSync &&
          other.entidade == this.entidade &&
          other.cursor == this.cursor);
}

class CursoresSyncCompanion extends UpdateCompanion<CursorSync> {
  final Value<String> entidade;
  final Value<int> cursor;
  final Value<int> rowid;
  const CursoresSyncCompanion({
    this.entidade = const Value.absent(),
    this.cursor = const Value.absent(),
    this.rowid = const Value.absent(),
  });
  CursoresSyncCompanion.insert({
    required String entidade,
    this.cursor = const Value.absent(),
    this.rowid = const Value.absent(),
  }) : entidade = Value(entidade);
  static Insertable<CursorSync> custom({
    Expression<String>? entidade,
    Expression<int>? cursor,
    Expression<int>? rowid,
  }) {
    return RawValuesInsertable({
      if (entidade != null) 'entidade': entidade,
      if (cursor != null) 'cursor': cursor,
      if (rowid != null) 'rowid': rowid,
    });
  }

  CursoresSyncCompanion copyWith(
      {Value<String>? entidade, Value<int>? cursor, Value<int>? rowid}) {
    return CursoresSyncCompanion(
      entidade: entidade ?? this.entidade,
      cursor: cursor ?? this.cursor,
      rowid: rowid ?? this.rowid,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (entidade.present) {
      map['entidade'] = Variable<String>(entidade.value);
    }
    if (cursor.present) {
      map['cursor'] = Variable<int>(cursor.value);
    }
    if (rowid.present) {
      map['rowid'] = Variable<int>(rowid.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('CursoresSyncCompanion(')
          ..write('entidade: $entidade, ')
          ..write('cursor: $cursor, ')
          ..write('rowid: $rowid')
          ..write(')'))
        .toString();
  }
}

abstract class _$OmegaDb extends GeneratedDatabase {
  _$OmegaDb(QueryExecutor e) : super(e);
  $OmegaDbManager get managers => $OmegaDbManager(this);
  late final $MensagensLocaisTable mensagensLocais =
      $MensagensLocaisTable(this);
  late final $CursoresSyncTable cursoresSync = $CursoresSyncTable(this);
  @override
  Iterable<TableInfo<Table, Object?>> get allTables =>
      allSchemaEntities.whereType<TableInfo<Table, Object?>>();
  @override
  List<DatabaseSchemaEntity> get allSchemaEntities =>
      [mensagensLocais, cursoresSync];
}

typedef $$MensagensLocaisTableCreateCompanionBuilder = MensagensLocaisCompanion
    Function({
  required String id,
  required String conversaId,
  required String papel,
  required String conteudo,
  Value<DateTime> criadoEm,
  Value<int> versaoSync,
  Value<int> rowid,
});
typedef $$MensagensLocaisTableUpdateCompanionBuilder = MensagensLocaisCompanion
    Function({
  Value<String> id,
  Value<String> conversaId,
  Value<String> papel,
  Value<String> conteudo,
  Value<DateTime> criadoEm,
  Value<int> versaoSync,
  Value<int> rowid,
});

class $$MensagensLocaisTableFilterComposer
    extends Composer<_$OmegaDb, $MensagensLocaisTable> {
  $$MensagensLocaisTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<String> get id => $composableBuilder(
      column: $table.id, builder: (column) => ColumnFilters(column));

  ColumnFilters<String> get conversaId => $composableBuilder(
      column: $table.conversaId, builder: (column) => ColumnFilters(column));

  ColumnFilters<String> get papel => $composableBuilder(
      column: $table.papel, builder: (column) => ColumnFilters(column));

  ColumnFilters<String> get conteudo => $composableBuilder(
      column: $table.conteudo, builder: (column) => ColumnFilters(column));

  ColumnFilters<DateTime> get criadoEm => $composableBuilder(
      column: $table.criadoEm, builder: (column) => ColumnFilters(column));

  ColumnFilters<int> get versaoSync => $composableBuilder(
      column: $table.versaoSync, builder: (column) => ColumnFilters(column));
}

class $$MensagensLocaisTableOrderingComposer
    extends Composer<_$OmegaDb, $MensagensLocaisTable> {
  $$MensagensLocaisTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<String> get id => $composableBuilder(
      column: $table.id, builder: (column) => ColumnOrderings(column));

  ColumnOrderings<String> get conversaId => $composableBuilder(
      column: $table.conversaId, builder: (column) => ColumnOrderings(column));

  ColumnOrderings<String> get papel => $composableBuilder(
      column: $table.papel, builder: (column) => ColumnOrderings(column));

  ColumnOrderings<String> get conteudo => $composableBuilder(
      column: $table.conteudo, builder: (column) => ColumnOrderings(column));

  ColumnOrderings<DateTime> get criadoEm => $composableBuilder(
      column: $table.criadoEm, builder: (column) => ColumnOrderings(column));

  ColumnOrderings<int> get versaoSync => $composableBuilder(
      column: $table.versaoSync, builder: (column) => ColumnOrderings(column));
}

class $$MensagensLocaisTableAnnotationComposer
    extends Composer<_$OmegaDb, $MensagensLocaisTable> {
  $$MensagensLocaisTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<String> get id =>
      $composableBuilder(column: $table.id, builder: (column) => column);

  GeneratedColumn<String> get conversaId => $composableBuilder(
      column: $table.conversaId, builder: (column) => column);

  GeneratedColumn<String> get papel =>
      $composableBuilder(column: $table.papel, builder: (column) => column);

  GeneratedColumn<String> get conteudo =>
      $composableBuilder(column: $table.conteudo, builder: (column) => column);

  GeneratedColumn<DateTime> get criadoEm =>
      $composableBuilder(column: $table.criadoEm, builder: (column) => column);

  GeneratedColumn<int> get versaoSync => $composableBuilder(
      column: $table.versaoSync, builder: (column) => column);
}

class $$MensagensLocaisTableTableManager extends RootTableManager<
    _$OmegaDb,
    $MensagensLocaisTable,
    MensagemLocal,
    $$MensagensLocaisTableFilterComposer,
    $$MensagensLocaisTableOrderingComposer,
    $$MensagensLocaisTableAnnotationComposer,
    $$MensagensLocaisTableCreateCompanionBuilder,
    $$MensagensLocaisTableUpdateCompanionBuilder,
    (
      MensagemLocal,
      BaseReferences<_$OmegaDb, $MensagensLocaisTable, MensagemLocal>
    ),
    MensagemLocal,
    PrefetchHooks Function()> {
  $$MensagensLocaisTableTableManager(_$OmegaDb db, $MensagensLocaisTable table)
      : super(TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$MensagensLocaisTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$MensagensLocaisTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$MensagensLocaisTableAnnotationComposer($db: db, $table: table),
          updateCompanionCallback: ({
            Value<String> id = const Value.absent(),
            Value<String> conversaId = const Value.absent(),
            Value<String> papel = const Value.absent(),
            Value<String> conteudo = const Value.absent(),
            Value<DateTime> criadoEm = const Value.absent(),
            Value<int> versaoSync = const Value.absent(),
            Value<int> rowid = const Value.absent(),
          }) =>
              MensagensLocaisCompanion(
            id: id,
            conversaId: conversaId,
            papel: papel,
            conteudo: conteudo,
            criadoEm: criadoEm,
            versaoSync: versaoSync,
            rowid: rowid,
          ),
          createCompanionCallback: ({
            required String id,
            required String conversaId,
            required String papel,
            required String conteudo,
            Value<DateTime> criadoEm = const Value.absent(),
            Value<int> versaoSync = const Value.absent(),
            Value<int> rowid = const Value.absent(),
          }) =>
              MensagensLocaisCompanion.insert(
            id: id,
            conversaId: conversaId,
            papel: papel,
            conteudo: conteudo,
            criadoEm: criadoEm,
            versaoSync: versaoSync,
            rowid: rowid,
          ),
          withReferenceMapper: (p0) => p0
              .map((e) => (e.readTable(table), BaseReferences(db, table, e)))
              .toList(),
          prefetchHooksCallback: null,
        ));
}

typedef $$MensagensLocaisTableProcessedTableManager = ProcessedTableManager<
    _$OmegaDb,
    $MensagensLocaisTable,
    MensagemLocal,
    $$MensagensLocaisTableFilterComposer,
    $$MensagensLocaisTableOrderingComposer,
    $$MensagensLocaisTableAnnotationComposer,
    $$MensagensLocaisTableCreateCompanionBuilder,
    $$MensagensLocaisTableUpdateCompanionBuilder,
    (
      MensagemLocal,
      BaseReferences<_$OmegaDb, $MensagensLocaisTable, MensagemLocal>
    ),
    MensagemLocal,
    PrefetchHooks Function()>;
typedef $$CursoresSyncTableCreateCompanionBuilder = CursoresSyncCompanion
    Function({
  required String entidade,
  Value<int> cursor,
  Value<int> rowid,
});
typedef $$CursoresSyncTableUpdateCompanionBuilder = CursoresSyncCompanion
    Function({
  Value<String> entidade,
  Value<int> cursor,
  Value<int> rowid,
});

class $$CursoresSyncTableFilterComposer
    extends Composer<_$OmegaDb, $CursoresSyncTable> {
  $$CursoresSyncTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<String> get entidade => $composableBuilder(
      column: $table.entidade, builder: (column) => ColumnFilters(column));

  ColumnFilters<int> get cursor => $composableBuilder(
      column: $table.cursor, builder: (column) => ColumnFilters(column));
}

class $$CursoresSyncTableOrderingComposer
    extends Composer<_$OmegaDb, $CursoresSyncTable> {
  $$CursoresSyncTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<String> get entidade => $composableBuilder(
      column: $table.entidade, builder: (column) => ColumnOrderings(column));

  ColumnOrderings<int> get cursor => $composableBuilder(
      column: $table.cursor, builder: (column) => ColumnOrderings(column));
}

class $$CursoresSyncTableAnnotationComposer
    extends Composer<_$OmegaDb, $CursoresSyncTable> {
  $$CursoresSyncTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<String> get entidade =>
      $composableBuilder(column: $table.entidade, builder: (column) => column);

  GeneratedColumn<int> get cursor =>
      $composableBuilder(column: $table.cursor, builder: (column) => column);
}

class $$CursoresSyncTableTableManager extends RootTableManager<
    _$OmegaDb,
    $CursoresSyncTable,
    CursorSync,
    $$CursoresSyncTableFilterComposer,
    $$CursoresSyncTableOrderingComposer,
    $$CursoresSyncTableAnnotationComposer,
    $$CursoresSyncTableCreateCompanionBuilder,
    $$CursoresSyncTableUpdateCompanionBuilder,
    (CursorSync, BaseReferences<_$OmegaDb, $CursoresSyncTable, CursorSync>),
    CursorSync,
    PrefetchHooks Function()> {
  $$CursoresSyncTableTableManager(_$OmegaDb db, $CursoresSyncTable table)
      : super(TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$CursoresSyncTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$CursoresSyncTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$CursoresSyncTableAnnotationComposer($db: db, $table: table),
          updateCompanionCallback: ({
            Value<String> entidade = const Value.absent(),
            Value<int> cursor = const Value.absent(),
            Value<int> rowid = const Value.absent(),
          }) =>
              CursoresSyncCompanion(
            entidade: entidade,
            cursor: cursor,
            rowid: rowid,
          ),
          createCompanionCallback: ({
            required String entidade,
            Value<int> cursor = const Value.absent(),
            Value<int> rowid = const Value.absent(),
          }) =>
              CursoresSyncCompanion.insert(
            entidade: entidade,
            cursor: cursor,
            rowid: rowid,
          ),
          withReferenceMapper: (p0) => p0
              .map((e) => (e.readTable(table), BaseReferences(db, table, e)))
              .toList(),
          prefetchHooksCallback: null,
        ));
}

typedef $$CursoresSyncTableProcessedTableManager = ProcessedTableManager<
    _$OmegaDb,
    $CursoresSyncTable,
    CursorSync,
    $$CursoresSyncTableFilterComposer,
    $$CursoresSyncTableOrderingComposer,
    $$CursoresSyncTableAnnotationComposer,
    $$CursoresSyncTableCreateCompanionBuilder,
    $$CursoresSyncTableUpdateCompanionBuilder,
    (CursorSync, BaseReferences<_$OmegaDb, $CursoresSyncTable, CursorSync>),
    CursorSync,
    PrefetchHooks Function()>;

class $OmegaDbManager {
  final _$OmegaDb _db;
  $OmegaDbManager(this._db);
  $$MensagensLocaisTableTableManager get mensagensLocais =>
      $$MensagensLocaisTableTableManager(_db, _db.mensagensLocais);
  $$CursoresSyncTableTableManager get cursoresSync =>
      $$CursoresSyncTableTableManager(_db, _db.cursoresSync);
}
