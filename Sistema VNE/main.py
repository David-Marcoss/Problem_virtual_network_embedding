from grafos import * 
from algoritimo_genetico import *
import networkx as nx
import time


def menu():

    print('---'*30)

    print("1- Ver rede fisica")
    print("2- Acrecentar recursos a nos e enlaces rede fisica")
    print("3- Ver requisicoes mapeadas")
    print("4- Incorporar rede virtual(Algoritimo genetico sequencial)")
    print("5- Incorporar rede virtual(Algoritimo genetico paralelo)")
    print("6- Incorporar rede virtual(Processamento de requisições Paralela)")
    print("7- Estatisticas")
    print("8- Sair")
    
    print('---'*30)
    
    n =  input("Escolha uma opcao:  ")
    print('---'*30)

    return n


def menu2():

    print('---'*30)

    print("1- Acrescentar recurso a cpu")
    print("2- Acrescentar recurso a enlace")
    print("3- Sair")
    
    print('---'*30)
    
    n =  input("Escolha uma opcao:  ")
    print('---'*30)

    return n

def mostrar_req_mapeadas(req_mapeadas):
    
    if req_mapeadas == []:
        print("\nNão a requisicoes mapeadas!!!\n")
    else:
        for i in range(len(req_mapeadas)):
            print('---'*30)
            print(f"Requisicao {i+1}: ")
            print(f"Rede Virtual: \nnos:{req_mapeadas[i][0].nodes()}\n enlaces: {req_mapeadas[i][0].edges()}\n")
            print(f"Mapeamento da requisição na Rede Fisica:\n nos:{req_mapeadas[i][1]}\n enlaces: {req_mapeadas[i][2]}\n")
            
            print('---'*30)

def nos_enlaces_mapeados(req_mapeadas):
    t_nos = 0
    t_enlaces = 0

    for i in req_mapeadas:
        t_nos += len(i[1])
        t_enlaces += len(i[2])
    
    return t_nos,t_enlaces


if __name__ == '__main__':

    rd_fisica = criar_rd_fisica()

    req_mapeadas = []
    req_nao_atendidas = 0
    req_atendidas = 0

    
    while(1):

        n = menu()

        if n == '1':
            plotar_rede(rd_fisica)
        
        if n == '2':

            while(1):
                n2 = menu2()

                if n2 == '1':
                    no = int(input("digite o numero do no: "))
                    recurso = int(input("digite a quantidade de recursos: "))

                    if no < 0 or recurso < 0:
                        print("\nNao foi possivel concluir a operacao !!!Digite um valor valido!!!\n")
                    else:

                        if adiciona_recurso_cpu(rd_fisica,no,recurso):
                            print("\nOperacao concluida com sucesso!!!\n")
                        else:
                            print("\nNao foi possivel concluir a operacao !!! No nao encontrado na rede !!!\n")

                
                if n2 == '2':
                    
                    no1 = int(input("digite o numero do no1: "))
                    no2 = int(input("digite o numero do no2: "))

                    recurso = int(input("digite a quantidade de recursos: "))

                    if no1 < 0 or no2 < 0 or recurso < 0:
                        print("\nNao foi possivel concluir a operacao !!!Digite um valor valido!!!\n")
                    else:

                        if adiciona_recurso_enlace(rd_fisica,no1,no2,recurso):
                            print("\nOperacao concluida com sucesso!!!\n")
                        else:
                            print("\nNao foi possivel concluir a operacao !!! Enlace nao encontrado na rede !!!\n")

                if n2 == '3':
                    break
                
                else:
                    pass


        if n == '3':
            mostrar_req_mapeadas(req_mapeadas)
        
        if n == '4':
            requisicao = input("Digite o nome do arquivo: ")
            requisicoes = cria_rede_virtual(requisicao)
            
            if(requisicoes):

                tempo_inicial = time.process_time()

                req_mapeadas,req_atendidas,req_nao_atendidas = processamento_requisicoes_sequencial(requisicoes,rd_fisica,req_mapeadas,req_atendidas,req_nao_atendidas)
                
                tempo_final = time.process_time()
                
                print("\nProcessamenrto sequencial:")
                print(f"Tempo total de cpu gasto para processar requisicoes: {tempo_final-tempo_inicial} segundos\n")

            else:
                print("\n Arquivo nao encontrado!!! digite um arquivo valido\n")
        
        if n == '5':
            requisicao = input("Digite o nome do arquivo: ")
            requisicoes = cria_rede_virtual(requisicao)
            
            if(requisicoes):
                tempo_inicial = time.process_time()

                req_mapeadas,req_atendidas,req_nao_atendidas = processamento_requisicoes_algoritimo_genetico_paralelo(requisicoes,rd_fisica,req_mapeadas,req_atendidas,req_nao_atendidas)
                
                tempo_final = time.process_time()
                
                print("\nProcessamenrto paralelo:")
                print(f"Tempo total de cpu gasto para processar requisicoes: {tempo_final-tempo_inicial} segundos\n")

            else:
                print("\n Arquivo nao encontrado!!! digite um arquivo valido\n")
        
        
        if n == '6':
            requisicao = input("Digite o nome do arquivo: ")
            requisicoes = cria_rede_virtual(requisicao)
            
            if(requisicoes):
                tempo_inicial = time.process_time()

                req_mapeadas,req_atendidas,req_nao_atendidas = processamento_requisicoes_paralelas(requisicoes,rd_fisica,req_mapeadas,req_atendidas,req_nao_atendidas)
                
                tempo_final = time.process_time()
                
                print("\nProcessamenrto paralelo:")
                print(f"Tempo total de cpu gasto para processar requisicoes: {tempo_final-tempo_inicial} segundos\n")

            else:
                print("\n Arquivo nao encontrado!!! digite um arquivo valido\n")
            
        if n == '7':
            print(f"\nTotal requisicoes: {req_atendidas+req_nao_atendidas}")
            print(f"\nrequisicoes atendidas: {req_atendidas}")
            print(f"requisicoes nao atendidas: {req_nao_atendidas}")

            if (req_atendidas+req_nao_atendidas > 0):            
                print(f"Taixa de requisições atendidas: {int((req_atendidas / (req_atendidas+req_nao_atendidas) * 100))}%")
            else:
                print(f"Taixa de requisições atendidas: 0%")

            t_nos,t_enlace = nos_enlaces_mapeados(req_mapeadas)
            print(f"Total de nos fisicos mapeados para requisicoes: {t_nos}") 
            print(f"Total de enlaces fisicos mapeados para requisicoes: {t_enlace}\n") 
            
        if n == '8':
            print("\nSaindo..........\n") 
            break
        



