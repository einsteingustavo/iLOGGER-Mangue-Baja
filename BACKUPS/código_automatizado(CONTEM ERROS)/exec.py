import os
from shutil import copy, move
from glob import glob
from subprocess import run
from sys import exit


path = os.getcwd()  # caminho do arquivo atual
lista_bruta = glob(os.path.join(path+"/B", "*"))
lista_de_indices = []
arquivos_locais = glob(os.path.join(path, "*"))  # procura arquivos
nome_runs_traduzidas = "RUNSTRADUZIDAS"


print(lista_bruta)


def verifica_arquivos():
    global lista_de_indices, lista_bruta, arquivos_locais

    # procura brutos
    pesquisa = False
    for endereco in arquivos_locais:
        if "B" in endereco:
            pesquisa = True

    if not pesquisa:
        print("Arquivo B faltando")
        return pesquisa

    # verifica integridade
    for x in lista_bruta:
        if not os.path.join(os.path.join(path, "B"), "RUN") in x:
            print("Arquivos mal formatados")
            return False
    print("Arquivos verificados!")

    return True

# Ajusta lista


def cria_lista():
    global lista_bruta, lista_de_indices
    for x in lista_bruta:
        if x[-3].isdigit():
            lista_de_indices.append(x[-3:])
        elif x[-2].isdigit():
            lista_de_indices.append(x[-2:])
        elif x[-1].isdigit():
            lista_de_indices.append(x[-1])
        else:
            print("fora de indice")
            input("enter para sair")
            exit()

# cria pastas (avs)


def cria_runs():
    global lista_de_indices, path, arquivos_locais, nome_runs_traduzidas

    # condição de exclusão
    boleano = False
    for x in arquivos_locais:
        if nome_runs_traduzidas in x:
            boleano = True

    if boleano:
        print(f"Exclua a pasta {nome_runs_traduzidas} e tente novamente")
        input()
        exit()

    os.mkdir(os.path.join(path, nome_runs_traduzidas))  # faz diretorio, vlw?

    # cria diretorios e distribui notebooks
    for indice in lista_de_indices:
        novo_path = os.path.join(
            path + "/" + nome_runs_traduzidas, "AV" + indice)
        # runs
        os.mkdir(novo_path)
        # notebooks
        copy("Generic-AV/AV10.ipynb", os.path.join(path + "/" +
             nome_runs_traduzidas, "AV" + indice) + "/AV10.ipynb")

    print("Arquivos criados!!!")


def distribui_csvs():
    global lista_de_indices, path
    for i in lista_de_indices:
        path_de_destino = os.path.join(
            path + "/" + nome_runs_traduzidas, "AV" + i)
        move(f"B/RUN{i}.csv", path_de_destino)


def salva_arquivos():
    global lista_de_indices

    arquivo = glob(os.path.join("Past-runs", "*"))
    if not arquivo:
        os.mkdir("Past-runs/antigo1")
    maior = 0
    for runs in arquivo:
        index = int(runs.replace("Past-runs/antigo", ""))
        if index > maior:
            maior = index
    maior += 1

    novo_antigo = f"Past-runs/antigo{maior}"

    os.mkdir(novo_antigo)

    for i in lista_de_indices:
        move(f"B/RUN{i}", novo_antigo)

# executa runs


if not verifica_arquivos():
    input()
    exit()
else:
    print("Escreva exatamente o numero de TODAS as runs do arquivo B")
    input("Aperte qualquer tecla para continuar")

cria_lista()
cria_runs()

run("./Generic-AV/source/exec", shell=True, check=True)

distribui_csvs()
salva_arquivos()

print("Finalizado!")
input()
