-- spark_desev.tabela_spark definition

-- Drop table

-- DROP TABLE spark_desev.tabela_spark;
CREATE SCHEMA spark_desev AUTHORIZATION postgres;

CREATE SEQUENCE spark_desev.tabela_spark2_id_seq START 1;


CREATE TABLE spark_desev.tabela_spark (
	id int4 NOT NULL DEFAULT nextval('spark_desev.tabela_spark2_id_seq'::regclass),
	npu text NULL,
	bloco_texto text NULL,
	caderno text NULL,
	data_caderno date NULL,
	lista_generica text NULL,
	processado bool NOT NULL,
	projeto text NOT NULL,
	lista_marcador text NULL,
	CONSTRAINT tabela_spark2_id_pkey PRIMARY KEY (id)
);
CREATE INDEX tabela_spark_projeto_idx ON spark_desev.tabela_spark USING btree (projeto);

CREATE TABLE spark_desev.processo (
	id bigserial NOT NULL,
	numero_processo varchar NULL,
	npu varchar NULL,
	grau int4 NULL,
	inquerito_policial varchar NULL,
	origem varchar NULL,
	protocolo varchar NULL,
	tipo_distribuicao varchar NULL,
	numero_ordem varchar NULL,
	CONSTRAINT processo_id_pkey PRIMARY KEY (id)
);
CREATE INDEX processo_npu_idx ON spark_desev.processo USING btree (npu);
CREATE INDEX processo_numero_processo_idx ON spark_desev.processo USING btree (numero_processo);

CREATE TABLE spark_desev.assunto (
	id bigserial NOT NULL,
	nome varchar NULL,
	cod_assunto varchar NULL,
	CONSTRAINT assunto_id_pkey PRIMARY KEY (id)
);
CREATE INDEX assunto_nome_idx ON spark_desev.assunto USING btree (nome);

CREATE table spark_desev.processo_assunto (
	processo_id bigserial NOT NULL,
	assunto_id bigserial NOT NULL,
	id bigserial NOT NULL,
	"data" date NULL,
	fonte_dado varchar NULL,
	CONSTRAINT id PRIMARY KEY (id),
	CONSTRAINT processo_assunto_assunto_fkey FOREIGN KEY (assunto_id) REFERENCES spark_desev.assunto(id),
	CONSTRAINT processo_assunto_processo_fkey FOREIGN KEY (processo_id) REFERENCES spark_desev.processo(id)
);
CREATE INDEX index_data ON spark_desev.processo_assunto USING btree (data);
CREATE INDEX index_processo_id ON spark_desev.processo_assunto USING btree (processo_id);
CREATE INDEX processo_assunto_idx ON spark_desev.processo_assunto USING btree (processo_id, assunto_id);

CREATE TABLE spark_desev.advogado (
	id bigserial NOT NULL,
	nome varchar NULL,
	numero_oab varchar NULL,
	CONSTRAINT advogado_id_pkey PRIMARY KEY (id)
);
CREATE INDEX nome_idx ON spark_desev.advogado USING btree (nome);
CREATE INDEX oab_idx ON spark_desev.advogado USING btree (numero_oab);

CREATE TABLE spark_desev.parte (
	id bigserial NOT NULL,
	nome varchar NULL,
	nome_corrigido varchar NULL,
	nome_abreviado varchar NULL,
	banco bool NULL,
	pessoa_juridica bool NULL,
	pessoa_fisica bool NULL,
	pequena_empresa bool NULL,
	governo bool NULL,
	cobranca bool NULL,
	CONSTRAINT parte_id_pkey PRIMARY KEY (id)
);
CREATE INDEX parte_nome_idx ON spark_desev.parte USING btree (nome);

CREATE SEQUENCE spark_desev.advogado_parte_processo_parte_id_seq START 1;

CREATE TABLE spark_desev.tipo_parte (
	id bigserial NOT NULL,
	nome varchar NULL,
	CONSTRAINT tipo_parte_id_pkey PRIMARY KEY (id)
);
CREATE INDEX index_nome_gin ON spark_desev.tipo_parte USING gin (nome gin_trgm_ops);

CREATE TABLE spark_desev.parte_processo (
	id bigserial NOT NULL,
	parte_id bigserial NOT NULL,
	processo_id bigserial NOT NULL,
	tipo_parte_id bigserial NOT NULL,
	CONSTRAINT parte_processo_id_pkey PRIMARY KEY (id),
	CONSTRAINT "parte_processo-tipo_parte_id" FOREIGN KEY (tipo_parte_id) REFERENCES spark_desev.tipo_parte(id),
	CONSTRAINT parte_processo_parte_id_fkey FOREIGN KEY (parte_id) REFERENCES spark_desev.parte(id),
	CONSTRAINT parte_processo_processo_id_fkey FOREIGN KEY (processo_id) REFERENCES spark_desev.processo(id)
);
CREATE INDEX parte_processo_id_idx ON spark_desev.parte_processo USING btree (id, parte_id, processo_id, tipo_parte_id);
CREATE INDEX parte_processo_idx ON spark_desev.parte_processo USING btree (parte_id, processo_id, tipo_parte_id);

CREATE TABLE spark_desev.advogado_parte_processo (
	id bigserial NOT NULL,
	advogado_id bigserial NOT NULL,
	parte_processo_id int8 NOT NULL DEFAULT nextval('spark_desev.advogado_parte_processo_parte_id_seq'::regclass),
	CONSTRAINT advogado_parte_processo_id_pkey PRIMARY KEY (id),
	CONSTRAINT advogado_parte_processo_advogado_fkey FOREIGN KEY (advogado_id) REFERENCES spark_desev.advogado(id),
	CONSTRAINT advogado_parte_processo_parte_processo_fkey FOREIGN KEY (parte_processo_id) REFERENCES spark_desev.parte_processo(id)
);

CREATE TABLE spark_desev.caderno (
	id bigserial NOT NULL,
	nome varchar NULL,
	CONSTRAINT caderno_id_pkey PRIMARY KEY (id)
);
CREATE INDEX caderno_nome_idx ON spark_desev.caderno USING btree (nome);

CREATE TABLE spark_desev.classe_processual (
	id bigserial NOT NULL,
	nome varchar NULL,
	nome_corrigido varchar NULL,
	CONSTRAINT classe_processual_id_fkey PRIMARY KEY (id)
);
CREATE INDEX classe_processual_nome_idx ON spark_desev.classe_processual USING btree (nome);

CREATE TABLE spark_desev.tribunal (
	id bigserial NOT NULL,
	nome varchar NULL,
	CONSTRAINT tribunal_id_pkey PRIMARY KEY (id)
);

CREATE TABLE spark_desev.tag (
	id bigserial NOT NULL,
	nome varchar NULL,
	CONSTRAINT tag_id_pkey PRIMARY KEY (id)
);

CREATE TABLE spark_desev.vara (
	id bigserial NOT NULL,
	nome varchar NULL,
	CONSTRAINT vara_id_pkey PRIMARY KEY (id)
);
CREATE INDEX vara_nome_idx ON spark_desev.vara USING btree (nome);

CREATE TABLE spark_desev.comarca (
	id bigserial NOT NULL,
	nome varchar NULL,
	tribunal_id int8 NULL,
	CONSTRAINT "comarca_id-pkey" PRIMARY KEY (id),
	CONSTRAINT comarca_tribunal_fkey FOREIGN KEY (tribunal_id) REFERENCES spark_desev.tribunal(id)
);
CREATE INDEX comarca_nome_idx ON spark_desev.comarca USING btree (nome);

CREATE TABLE spark_desev.data_distribuicao (
	id bigserial NOT NULL,
	"data" date NULL,
	CONSTRAINT data_distribuicao_id_pkey PRIMARY KEY (id)
);

CREATE TABLE spark_desev.foro (
	id bigserial NOT NULL,
	nome varchar NULL,
	CONSTRAINT foro_id_pkey PRIMARY KEY (id)
);

CREATE TABLE spark_desev.historico_dado (
	id bigserial NOT NULL,
	"data" date NULL,
	processo varchar NULL,
	observacao varchar NULL,
	CONSTRAINT historico_dado_id_pkey PRIMARY KEY (id)
);

CREATE TABLE spark_desev.magistrado (
	id bigserial NOT NULL,
	nome varchar NULL,
	CONSTRAINT magistrado_id_pkey PRIMARY KEY (id)
);

CREATE TABLE spark_desev.marcador (
	id bigserial NOT NULL,
	nome varchar NULL,
	CONSTRAINT marcador_id_pkey PRIMARY KEY (id)
);
CREATE INDEX marcador_nome_idx ON spark_desev.marcador USING btree (nome);

CREATE TABLE spark_desev.movimento (
	id bigserial NOT NULL,
	"data" date NULL,
	data_caderno date NULL,
	texto varchar NULL,
	hash_texto varchar NULL,
	processo_id bigserial NOT NULL,
	caderno varchar NULL,
	fonte_dado varchar NULL,
	magistrado_id bigserial NOT NULL,
	CONSTRAINT movimento_id_pkey PRIMARY KEY (id),
	CONSTRAINT movimento_magistrado_id_fkey FOREIGN KEY (magistrado_id) REFERENCES spark_desev.magistrado(id) ON DELETE CASCADE,
	CONSTRAINT movimento_processo_id_fkey FOREIGN KEY (processo_id) REFERENCES spark_desev.processo(id)
);
CREATE INDEX fki_acompanhamento_processual_processo_id_fkey ON spark_desev.movimento USING btree (processo_id);
CREATE INDEX hash_texto_idx ON spark_desev.movimento USING btree (hash_texto);

CREATE TABLE spark_desev.movimento_marcador (
	id bigserial NOT NULL,
	movimento_id bigserial NOT NULL,
	marcador_id bigserial NOT NULL,
	CONSTRAINT movimento_marcador_id_pkey PRIMARY KEY (id),
	CONSTRAINT movimento_marcador_marcador_fkey FOREIGN KEY (marcador_id) REFERENCES spark_desev.marcador(id),
	CONSTRAINT movimento_marcador_movimento_fkey FOREIGN KEY (movimento_id) REFERENCES spark_desev.movimento(id)
);
CREATE INDEX movimento_marcador_idx ON spark_desev.movimento_marcador USING btree (movimento_id, marcador_id);

-- etapas processo
CREATE TABLE spark_desev.processo_caderno (
	id bigserial NOT NULL,
	processo_id bigserial NOT NULL,
	caderno_id bigserial NOT NULL,
	CONSTRAINT processo_caderno_id_pkey PRIMARY KEY (id),
	CONSTRAINT caderno_id FOREIGN KEY (caderno_id) REFERENCES spark_desev.caderno(id),
	CONSTRAINT processo_id FOREIGN KEY (processo_id) REFERENCES spark_desev.processo(id)
);
CREATE INDEX processo_caderno_idx ON spark_desev.processo_caderno USING btree (processo_id, caderno_id);


CREATE SEQUENCE spark_desev.processo_classe_processual_classe_id_seq START 1;


CREATE TABLE spark_desev.processo_classe_processual (
	id bigserial NOT NULL,
	processo_id bigserial NOT NULL,
	classe_processual_id int8 NOT NULL DEFAULT nextval('spark_desev.processo_classe_processual_classe_id_seq'::regclass),
	fonte_dado varchar NULL,
	"data" date NULL,
	CONSTRAINT processo_classe_processual_id_pkey PRIMARY KEY (id),
	CONSTRAINT processo_classe_classe_fkey FOREIGN KEY (classe_processual_id) REFERENCES spark_desev.classe_processual(id),
	CONSTRAINT processo_classe_processo_fkey FOREIGN KEY (processo_id) REFERENCES spark_desev.processo(id)
);
CREATE INDEX processo_classe_idx ON spark_desev.processo_classe_processual USING btree (processo_id, classe_processual_id);

CREATE TABLE spark_desev.processo_comarca (
	id bigserial NOT NULL,
	processo_id bigserial NOT NULL,
	comarca_id bigserial NOT NULL,
	fonte_dado varchar NULL,
	"data" date NULL,
	CONSTRAINT processo_comarca_id_pkey PRIMARY KEY (id),
	CONSTRAINT processo_comarca_comarca_id_fkey FOREIGN KEY (comarca_id) REFERENCES spark_desev.comarca(id),
	CONSTRAINT processo_comarca_processo_id_fkey FOREIGN KEY (processo_id) REFERENCES spark_desev.processo(id)
);
CREATE INDEX processo_comarca_idx ON spark_desev.processo_comarca USING btree (processo_id, comarca_id);

CREATE TABLE spark_desev.processo_data_distribuicao (
	id bigserial NOT NULL,
	processo_id bigserial NOT NULL,
	data_distribuicao_id bigserial NOT NULL,
	CONSTRAINT processo_data_distribuicao_id_pkey PRIMARY KEY (id),
	CONSTRAINT processo_data_distribuicao_data_id_pkey FOREIGN KEY (data_distribuicao_id) REFERENCES spark_desev.data_distribuicao(id),
	CONSTRAINT processo_data_distribuicao_processo_id_pkey FOREIGN KEY (processo_id) REFERENCES spark_desev.processo(id)
);
CREATE INDEX processo_data_distribuicao_idx ON spark_desev.processo_data_distribuicao USING btree (processo_id, data_distribuicao_id);

CREATE TABLE spark_desev.processo_foro (
	id bigserial NOT NULL,
	processo_id bigserial NOT NULL,
	foro_id bigserial NOT NULL,
	fonte_dado varchar NULL,
	"data" date NULL,
	CONSTRAINT processo_foro_id_pkey PRIMARY KEY (id),
	CONSTRAINT processo_foro_foro_id_fkey FOREIGN KEY (foro_id) references spark_desev.foro(id),
	CONSTRAINT processo_foro_processo_id_fkey FOREIGN KEY (processo_id) REFERENCES spark_desev.processo(id)
);
CREATE INDEX processo_foro_idx ON spark_desev.processo_foro USING btree (processo_id, foro_id);

CREATE TABLE spark_desev.processo_tag (
	id bigserial NOT NULL,
	processo_id bigserial NOT NULL,
	tag_id bigserial NOT NULL,
	CONSTRAINT processo_tag_id_pkey PRIMARY KEY (id),
	CONSTRAINT processo_tag_tag_fkey FOREIGN KEY (tag_id) REFERENCES spark_desev.tag(id),
	CONSTRAINT processo_tag_processo_fkey FOREIGN KEY (processo_id) REFERENCES spark_desev.processo(id)
);
CREATE INDEX processo_tag_idx ON spark_desev.processo_tag USING btree (processo_id, tag_id);

CREATE TABLE spark_desev.processo_vara (
	id bigserial NOT NULL,
	processo_id bigserial NOT NULL,
	vara_id bigserial NOT NULL,
	fonte_dado varchar NULL,
	"data" date NULL,
	CONSTRAINT processo_vara_id_pkey PRIMARY KEY (id),
	CONSTRAINT processo_vara_processo_id_fkey FOREIGN KEY (processo_id) REFERENCES spark_desev.processo(id),
	CONSTRAINT processo_vara_vara_id_fkey FOREIGN KEY (vara_id) REFERENCES spark_desev.vara(id)
);
CREATE INDEX processo_vara_idx ON spark_desev.processo_vara USING btree (processo_id, vara_id);

CREATE TABLE spark_desev.tabela_banco_julgados (
	id bigserial NOT NULL,
	numero_processo varchar NULL,
	assunto varchar NULL,
	magistrado varchar NULL,
	comarca varchar NULL,
	foro varchar NULL,
	vara varchar NULL,
	data_disponibilizacao date NULL,
	movimento varchar NULL,
	processado bool NOT NULL DEFAULT false,
	classe varchar NULL,
	CONSTRAINT tabela_banco_julgados_id_pkey PRIMARY KEY (id)
);
CREATE INDEX tabela_banco_julgados_processado_idx ON spark_desev.tabela_banco_julgados USING btree (processado);