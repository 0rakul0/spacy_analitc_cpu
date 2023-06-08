import re
from unicodedata import normalize
import time
import datetime
import socket
import collections
from difflib import SequenceMatcher
from functools import reduce,partial
import zipfile
import numpy as np
import pandas as pd
import pyspark
import urllib
from pyspark.shell import spark
from pyspark.sql.functions import *
from pyspark.ml.classification import *
from pyspark.ml.evaluation import *
from pyspark.ml.feature import *
from py4j.protocol import Py4JJavaError
from pyspark import SparkContext
from pyspark.sql import SparkSession # Create Spark config for our Kubernetes based cluster manager
import pyspark.sql.functions as psf # funções p/ operar dataframes
from pyspark.sql.types import * # data types do Spark SQL
import sys

from pyspark.sql.functions import *
# start Spark session

spark = pyspark.sql.SparkSession.builder.appName('Iris').getOrCreate()

# print runtime versions
print('****************')
print('Python version: {}'.format(sys.version))
print('Spark version: {}'.format(spark.version))
print('****************')

class Extrator_spark():
    def remove_acentos(self,txt):
        if not txt:
            return txt
        text = str((normalize('NFKD', txt).encode("ascii", errors="ignore")).decode("utf-8", errors="ignore"))
        return text.replace("'", "").replace('"', "")

    def remove_varios_espacos(self,txt):
        array = txt.split()
        return " ".join(array).strip()

    def flatten(self, pair):
        f, text = pair
        return [line.split(",") + [f] for line in text]

    def filtragem(self,tupla):  # Retorna apenas os blocos que contenham as palavras chaves contidas no regex
        match = re.findall("CLASSE\s*\:", tupla[1])
        return False if match else True
    def cria_lista_de_linhas(self,arquivo):
        lista_expressoes_ignoradas = []

        expressao_cabecalho = re.compile(
            '(DISPONIBILIZACAO\s*:?\s*.{0,9}?-?FEIRA\s*,?\s*)(\d{1,2}\s*DE\s*.{4,9}\s*DE\s*\d{4})', re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_cabecalho)

        expressao_diario = re.compile(r'DIARIO.{0,100}\s*-?\s*CADERNO\s*JUDICIAL\s*-?\s*2.\s*', re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_diario)

        expressao_caderno = re.compile(r'CADERNO\s*\d{1,2}\n?', re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_caderno)

        expressao_site = re.compile(r'WWW.DJE.TJSP.JUS.BR', re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_site)

        expressao_edicao = re.compile(r'SAO\s*PAULO\s*,?\s*ANO\s*\w*\s*-?\s*EDICAO\s*(\d+\s)*', re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_edicao)

        expressao_rodape = re.compile(
            r'F\s*E\s*D\s*E\s*R\s*A\s*L.{0,100}?1\s*1\s*\.\s*4\s*1\s*9\s*\/0\s*6\s*,?\s*A\s*R\s*T\s*\.\s*4', re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_rodape)

        expressao_rodape2 = re.compile(
            r'((?:PUBLICACAO\s*O\s*F\s*I\s*C\s*I\s*A\s*L\s*)?DO\s*TRIBUNAL\s*DE\s*JUSTICA\s*DO\s*ESTADO\s*DE\s*SAO\s*PAULO\s*-?\s*LEI\s*O\s*(?:DISPONIBILIZACAO\s*:?\s*.{0,9}?\s*-?FEIRA\s*,?\s*\d+\s*DE\s*.{1,10}\s*DE\s*\d{4})?\s*DIARIO\s*.*?CADERNO.*?(?:SAO\s*PAULO\s*,?\s*ANO\s*.*?EDICAO\s*(?:\d+\s*)*|PARTE\s*\w+\s*(?:\d+)?\s*))',
            re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_rodape2)

        #     expressao_cabecalho2 = re.compile(r'(PUBLICACAO\s*O\s*F\s*I\s*C\s*I\s*A\s*L\s*DO\s*TRIBUNAL\s*DE\s*JUSTICA\s*DO\s*.*?\s*DISPONIBILIZACAO\s*:\s*.{0,9}?\-?FEIRA\s*\,?\s*\d+\s*DE\s*.*?\s*DIARIO\s*DA\s*JUSTICA\s*.*?\s*PARTE\s*\w+\s*.*?\s*EDICAO(?:\s*\d+)+)', re.IGNORECASE)
        # expressao_cabecalho2 = re.compile(r'(PUBLICACAO\s*O\s*F\s*I\s*C\s*I\s*A\s*L\s*DO\s*TRIBUNAL\s*DE\s*JUSTICA\s*DO\s*ESTADO\s*DE\s*SAO\s*PAULO.*?LEI\s*FEDERAL\s*N.?\s*\d*\.?\d*\/\d*.?\s*ART.?\s*\d*.?\s*DISPONIBILIZACAO\s*:\s*.{0,9}?\-?FEIRA\s*\,?\s*\d+\s*DE\s*.*?\s*DIARIO\s*DA\s*JUSTICA\s*.*?\s*PARTE\s*\w+\s*.*?\s*EDICAO(?:\s*\d+)+)', re.IGNORECASE)
        expressao_cabecalho2 = re.compile(
            r'(PUBLICACAO\s*O\s*F\s*I\s*C\s*I\s*A\s*L\s*DO\s*TRIBUNAL\s*DE\s*JUSTICA\s*DO\s*ESTADO\s*DE\s*SAO\s*PAULO.{0,40}LEI FEDERAL\s*N.?\s*\d*\.?\d*\/\d*.?\s*ART.?\s*\d*.?\s*DISPONIBILIZACAO\s*:\s*.{0,9}?\-?FEIRA\s*\,?\s*\d+\s*DE\s*.{0,50}\s*DIARIO\s*DA\s*JUSTICA\s*.{0,100}\s*PARTE\s*\w+\s*.{0,60}\s*EDICAO(?:\s*\d+)+)',
            re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_cabecalho2)

        expressao_cabecalho3 = re.compile(
            r'PUBLICACAO\s*.{1,30}?\s*DO\s*TRIBUNAL\s*.{1,150}?\s*CADERNO\s*JUD\s*.{1,50}?\s*(?:CAPITAL|INTERIOR)',
            re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_cabecalho3)

        expressao_cabecalho4 = re.compile(r'PUBLICACAO\s*.{1,20}?\s*DO\s*TRIBUNAL\s*.{1,150}?\s*LEI\s*O', re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_cabecalho4)

        expressao_cabecalho5 = re.compile(r'DIARIO\s*.{1,50}?\s*CADERNO\s*JUD\s*.{1,100}?\s*CAPITAL\s*', re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_cabecalho5)

        expressao_cabecalho6 = re.compile(
            r'(?:(?:\s*\d+\s*))?\s*D.?O.?E.?\s*\;?\s*PODER\s*.{1,50}?\s*SAO\s*PAULO\s*.{1,50}?\s*DE\s*.{1,15}?\s*DE\s*\d{4}\s*.{0,50}\s*\—?\s*.{0,20}?\s*(?:(?:\s*\d+\s*))?',
            re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_cabecalho6)

        expressao_cabecalho7 = re.compile(
            r'DIARIO\W*OFI\W*CIAL\W*PODER\W*JUD\w*\W*CAD\w*\W*JUD\w*.{1,80}?\W*(?:CAPITAL|INTERIOR)\W*(?:\d+|\W*(?:PARTE|P\w*)\W*\w*)',
            re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_cabecalho7)

        # cadernos antigos
        expressao_cabecalho8 = re.compile(
            r'\w*\-?FEIRA\W*\d+.{0,50}?\W*S.O\W*PAULO\W*.{0,50}?\W*(?:\d+)?\W*DI.RIO\W*OFI\w*.{0,50}?(?:PARTE|PRT)\W*I+\W*(?:\d+\/?\d+)?',
            re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_cabecalho8)

        expressao_cabecalho9 = re.compile(
            r'\w*\W*\—?\W*D.O.E.\W*.{0,50}?\W*S.O\W*PAULO\W*.{0,50}?\w+\-FEIRA\W*\d+\W*.{0,20}\W*DE\W*\d{4}\W*(?:CADERNO\W*\d+\W*\d*)?',
            re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_cabecalho9)

        expressao_cabecalho10 = re.compile(
            r'PUBLICACAO\W*OFICIAL\W*DO\W*TRIBUNAL\W*DE\W*JUSTICA\W*DO\W*ESTADO\W*DE\W*S.O\W*PAULO\W*LEI\W*O\W*DI.RIO\W*DA\W*JUSTI.A\W*ELETR.NICO\W*CADERNO\W*JUDICIAL\W*1A\W*INST.NCIA\W*(?:INTERIOR|CAPITAL)\W*(?:PARTE\W*\w*)?\W*\W*\d+',
            re.IGNORECASE)
        lista_expressoes_ignoradas.append(expressao_cabecalho10)

        separador = '(?:\s+SEPARDOR_BLOCO\s+(?:PROC\s*\.?\s*?(?:ESSO)?(?:[ \:\s*\-\s*]*))?(\\b\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{3}\s*[\.\-]\s*\d{4}|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{4}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{4}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{5}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{7}\s*[\.\-]\s*\d\/\d|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{3}\s*[\.\-]\s*\d{3}\s*[\.\-]\s*\d\/\d|\\b\d{6,7}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{6}(\s*[\.\-]\s*\d\/\d{6}\s*[\.\-]\s*\d{3})?|\\b\d{3}\.\d{2,4}\.\d{6}\-?\d?))'

        return self.cria_lista_de_linhas_mantendo_separador(arquivo, lista_expressoes_ignoradas, separador)


    def cria_lista_de_linhas_mantendo_separador(self,arquivo, lista_expressoes_ignoradas, separador):
        # Separa o arquivo por blocos de acordo com o separador

        # lista_expressoes_ignoradas = []
        linhas = arquivo[1:]  # 0 é o nome do arquivo e 1 é o texto em si
        nome_arquivo = arquivo[0]
        if linhas != []:

            linhas = ''.join(linhas).split('\n')
            linhas = list(map(lambda linha: self.remove_acentos(linha).upper(), linhas))

            linhas = list(filter(lambda linha: linha != '',
                                 list(map(lambda linha: self.remove_varios_espacos(re.sub('\s*\n|\t', '', linha)), linhas))))
            linhas = list(map(lambda linha: linha + ' SEPARDOR_BLOCO ', linhas))

            # linhas = list(map(lambda x:x.replace('\n',' '), linhas))
            # linhas = corrige_linhas_separador(linhas)
            linhas_concatenadas = ''
            fatia = 10000
            for i in range(0, int(len(linhas) / fatia) + 1):
                if i * fatia < len(linhas):
                    linhas_concatenadas += (self.remove_acentos(
                        reduce(lambda x, y: x + ' ' + y if not x.endswith('-') else x[:-1] + y,
                               linhas[i * fatia:i * fatia + fatia]))).upper()

            for expressao_ignorada in lista_expressoes_ignoradas:
                linhas_concatenadas = expressao_ignorada.sub('', linhas_concatenadas)

            lista_de_linhas = re.split(separador, linhas_concatenadas)
            lista_de_linhas = list(map(lambda linha: re.sub('\sSEPARDOR_BLOCO\s', ' ', linha),
                                       list(filter(lambda linha: linha is not None, lista_de_linhas))))[1:]
            lista_de_linhas = list(filter(lambda linha: linha != ' ', lista_de_linhas))
            lista_de_linhas = list(filter(lambda linha: linha != ' (', lista_de_linhas))
            lista_de_linhas = list(filter(
                lambda linha: linha != re.search('\A\/\d{2}\s*\(\s*$', linha).group(0) if re.search('\A\/\d{2}\s*\(\s*$',
                                                                                                    linha) else ' ',
                lista_de_linhas))
            lista_de_linhas = list(filter(lambda linha: len(linha) > 3, lista_de_linhas))

            regex_npu = re.compile(
                '^(\\b\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{3}\s*[\.\-]\s*\d{4}|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{4}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{4}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{5}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{7}\s*[\.\-]\s*\d\/\d|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{3}\s*[\.\-]\s*\d{3}\s*[\.\-]\s*\d\/\d|\\b\d{6,7}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{6}(\s*[\.\-]\s*\d\/\d{6}\s*[\.\-]\s*\d{3})?|\\b\d{3}\.\d{2,4}\.\d{6}\-?\d?)$')

            for pos, linha in enumerate(lista_de_linhas):
                npu = True
                while npu:
                    if re.search(regex_npu, lista_de_linhas[pos]) and re.search(regex_npu, lista_de_linhas[pos + 1]):
                        lista_de_linhas.pop(pos + 1)
                    else:
                        npu = False

            novas_linhas = []

            # For para mesclar a posição i+1 com a posição i, onde i é o texto e i+1 é o npu
            for pos, linha in enumerate(lista_de_linhas):
                if pos % 2 == 0:
                    try:
                        novas_linhas.append(f'{linha} {lista_de_linhas[pos + 1]}')
                    except:
                        continue

            # lista_de_linhas = list(map(lambda linha: linha.upper(), lista_de_linhas))
            # return (nome_arquivo,lista_de_linhas)
            return (nome_arquivo, novas_linhas)

        return ('', '')

    def cria_lista_de_tuplas_arquivo_bloco(self,rdd):
        lista_de_tuplas = []
        for bloco in rdd[1]:
            lista_de_tuplas.append((rdd[0], bloco))
        return lista_de_tuplas

    def extrai_and_return_rdd(self, bucket, ano, mes):
        # Inicia contagem
        t = time.perf_counter()

        try:
            # allInOneRDD = sc.wholeTextFiles("data/").flatMap(lambda l:[line+","+f for line in c.splitlines()])
            arquivos = sc.wholeTextFiles(f"./temp/{bucket}/{ano}/{mes}", 2)
        except Py4JJavaError as e:
            print('Pasta não encontrada', e)
            return []
        matches_rdd = arquivos.filter(
            lambda caderno: re.search(r'JUD.*?\_(?:III|I\_PARTE\_I\b)|CADERNO(11|12|13|14|15|18)', caderno[0],
                                      flags=re.IGNORECASE))
        matches_rdd = matches_rdd.map(self.cria_lista_de_linhas)

        # Finaliza contagem de processamento
        elapsed = time.perf_counter() - t
        print(f'Time   {elapsed:0.4}')

        # Retorna assuntos
        return matches_rdd

    def lista_regex(self):
        lista_regex_sentencas = []
