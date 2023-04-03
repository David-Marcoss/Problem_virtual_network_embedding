import networkx as nx
from random import sample,randint,random
from thread import ThreadReturn

def mapeamento_dos_nos(lista_nos,rd_virtual,rd_fisica):
    map = []
    i = 0
    for edge in rd_virtual.edges():
        caminho = nx.single_source_shortest_path(rd_fisica, lista_nos[edge[0]])
        map.append(caminho[lista_nos[edge[1]]])
        i+=1

        #print(caminho)

    return map


def fitness(lista_nos,rd_fisica,rd_virtual):

    map = mapeamento_dos_nos(lista_nos,rd_virtual,rd_fisica)


    lista_enlaces = []
    nos_cobrados = []

    num_enlaces = 0
    pontuacao = 0
    punicao = 2
    total_cpu = 0
    total_enlace = 0
    
    enlaces_virtuais = list(rd_virtual.edges(data=True))

    for enlace in map:
        for i in range(len(enlace)-1):
            
            en = sorted([enlace[i],enlace[i+1]])

            if  (en in lista_enlaces):
                punicao += 1000    
            
            if (rd_fisica.get_edge_data(enlace[i],enlace[i+1])['weight'] >=  enlaces_virtuais[num_enlaces][2]['weight']) :

                total_enlace+= rd_fisica.get_edge_data(enlace[i],enlace[i+1])['weight'] - enlaces_virtuais[num_enlaces][2]['weight']
            else:
                punicao += 1000
            

            if enlace[i] not in nos_cobrados:
               
                if (rd_fisica.nodes[enlace[i]]['cpu'] >= rd_virtual.nodes[enlaces_virtuais[num_enlaces][0]]['cpu']):    
                    
                    total_cpu += rd_fisica.nodes[enlace[i]]['cpu'] - rd_virtual.nodes[enlaces_virtuais[num_enlaces][0]]['cpu']          
                    
                else:

                    punicao += 1000
                
                nos_cobrados.append(enlace[i])
                     
            if enlace[i+1] not in nos_cobrados:
                if(rd_fisica.nodes[enlace[i+1]]['cpu'] >= rd_virtual.nodes[enlaces_virtuais[num_enlaces][1]]['cpu']):
                    
                    total_cpu += rd_fisica.nodes[enlace[i+1]]['cpu'] - rd_virtual.nodes[enlaces_virtuais[num_enlaces][1]]['cpu']
                else:
                    punicao += 1000 
            
                nos_cobrados.append(enlace[i+1])

            lista_enlaces.append(en)     

        num_enlaces+=1

    enlaces_mapeados = len(lista_enlaces) - rd_virtual.number_of_edges()
    nos_mapeados = len(nos_cobrados) - rd_virtual.number_of_nodes()

    pontuacao += (total_cpu + total_enlace - punicao) / (pow(enlaces_mapeados + nos_mapeados,3)+1)

    
    return pontuacao

def crossover_uniforme(pai1, pai2):
    filho = []

    for i in range(len(pai1)):
        if random() < 0.5 and (pai1[i] not in(filho)):
            filho.append(pai1[i])
        else:
            if pai2[i] not in filho:
                filho.append(pai2[i])
            else:
                filho.append(pai1[i])
            
    return filho


def mutacao(lista_nos, prob_mutacao):
    if random() < prob_mutacao:
        pos1 = randint(0, len(lista_nos)-1)
        pos2 = randint(0, len(lista_nos)-1)

        lista_nos[pos1], lista_nos[pos2] = lista_nos[pos2], lista_nos[pos1]
    
    return lista_nos

def tournament_selection(pontuacao, k=4):
    pais = []
    for i in range(2):
        candidatos = sample(pontuacao, k)
        
        melhor = max(candidatos)
        
        pais.append(melhor[1])
    
    return pais

def gera_populacao(pop_size,rd_virtual,rd_fisica):

    nos_virtuais = len(rd_virtual.nodes)
    pop = []


    while(len(pop) < pop_size):
        nos_sorteados = sample(range(0, len(rd_fisica.nodes)), nos_virtuais)
        if nos_sorteados not in(pop):
            pop.append(nos_sorteados)
        #print(nos_sorteados)
    
    return pop

def calculo_fitness(populacao,rd_fisica,rd_virtual):
    pontuacao = []
    for i in populacao:
        pontuacao.append([fitness(i,rd_fisica,rd_virtual),i])
    
    return pontuacao


def evolucao(pontuacao):
        """
        Evolui a população para uma nova geração, retorna
        a população evoluida.
        """

        new_pop = []
        while len(new_pop) < len(pontuacao):
            
            pais = tournament_selection(pontuacao)

            filho = crossover_uniforme(pais[0],pais[1])
            filho = mutacao(filho,0.10)
    
            if filho not in new_pop and len(filho) == len(set(filho)):
                new_pop.append(filho)
        
        return new_pop 


def algoritimo_genetico(rd_fisica,rd_virtual):
    
    num_geracoes = 200
    pop_size = 700

    pop = gera_populacao(pop_size,rd_virtual,rd_fisica)


    for i in range(num_geracoes):
        
        pontuacao = calculo_fitness(pop,rd_fisica,rd_virtual)
        
        pontuacao = sorted(pontuacao,reverse=True)

        pop = [pontuacao[i][1] for i in range(10)] + evolucao(pontuacao[10:])

    
      #se a pontuação for negativa quer dizer que não foi encontrada um mapeamento
    if pontuacao[0][0] >= 0:    
        return [pontuacao[0][1],mapeamento_dos_nos(pontuacao[0][1],rd_virtual,rd_fisica)]
    else:
        return []

def evolucao_paralela(pontuacao):
    
    n = len(pontuacao)//4
    pop_evoluida = []
    
    i = 0
    j = 0
    threads = []
    
    for l in range(4):
        j+=n
        
        th_f = ThreadReturn(target=evolucao,args=(pontuacao[i:j],))

        th_f.start()

        threads.append(th_f)

        i+=n
    
    for th in threads:  
        new_pop = th.join()
        
        pop_evoluida+= new_pop
    
    return pop_evoluida

def algoritimo_genetico_paralelo(rd_fisica,rd_virtual):
    
    
    num_geracoes = 100
    pop_size = 1000

    pop = gera_populacao(pop_size,rd_virtual,rd_fisica)

    for i in range(num_geracoes):
        
        n = pop_size//4
        pontuacao = []
        
        i = 0
        j = 0
        threads = []
        
        for l in range(4):
            j+=n
            
            th_f = ThreadReturn(target=calculo_fitness,args=(pop[i:j],rd_fisica,rd_virtual))

            th_f.start()

            threads.append(th_f)

            i+=n
        
        for i in range(len(threads)):
            pt = threads[i].join()
            pontuacao += pt
        
        pontuacao = sorted(pontuacao,reverse=True)

        pop = [pontuacao[i][1] for i in range(10)] + evolucao_paralela(pontuacao[10:])
          
      #se a pontuação for negativa quer dizer que não foi encontrada um mapeamento
    if pontuacao[0][0] >= 0:    
        return [pontuacao[0][1],mapeamento_dos_nos(pontuacao[0][1],rd_virtual,rd_fisica)]
    else:
        return []


def consume_recursos(map,rd_fisica,rd_virtual):

    nos_cobrados = []
    enlaces = []

    num_enlaces = 0
    
    enlaces_virtuais = list(rd_virtual.edges(data=True))

    for enlace in map:
        for i in range(len(enlace)-1):
        
            #verifica se o no do enlace ja teve seu recurso de cpu contabilizado
            if enlace[i] not in nos_cobrados:
                    
                rd_fisica.nodes[enlace[i]]['cpu'] -= rd_virtual.nodes[enlaces_virtuais[num_enlaces][0]]['cpu']
                
                nos_cobrados.append(enlace[i])
        
            #faz a mesma operação acima so que com o outro no do enlace               
            if enlace[i+1] not in nos_cobrados:
                rd_fisica.nodes[enlace[i+1]]['cpu'] -= rd_virtual.nodes[enlaces_virtuais[num_enlaces][1]]['cpu']
                nos_cobrados.append(enlace[i+1])
                    
            rd_fisica.get_edge_data(enlace[i],enlace[i+1])['weight'] -= enlaces_virtuais[num_enlaces][2]['weight']

            enlaces.append(sorted((enlace[i],enlace[i+1])))
    
    return nos_cobrados,enlaces

def processamento_requisicoes_sequencial(requisicoes,rd_fisica,req_mapeadas,req_atendidas,req_nao_atendidas):
    
    
    """
        Faz o processamento sequencial das requisicoes 
    """

    i = 1

    for rd_virtual in requisicoes:
        
        print(f"\nRequisicao {i}: ")

        if (rd_virtual.number_of_nodes() > rd_fisica.number_of_edges() or 
            rd_virtual.number_of_nodes() > rd_fisica.number_of_edges()):

            print("\n A rede fisica não é capaz de atender essa requisicao!!!\n A rede virtual possui mais nos ou enlaces que a rede virtual!!\n")
            req_nao_atendidas += 1
        else:

            print("\nProcessando requisicao, aguarde um momento....\n")
            individuo_map = algoritimo_genetico(rd_fisica,rd_virtual)

            if individuo_map == []:
                print("\n A rede fisica não é capaz de atender essa requisicao!!!\nNao foi possivel encontrar um mapeamento valido para atender a requisição!!\n")   
                req_nao_atendidas += 1
            else:
                nos_mapeados,enlaces_mapeados = consume_recursos(individuo_map[1],rd_fisica,rd_virtual)
                print("\nIncorporação da rede virtual concluida com sucesso!!")
                print(f"Mapeamento da requisição na Rede Fisica:\n nos:{individuo_map[0]}\n enlaces: {individuo_map[1]}\n")

                req_mapeadas.append([rd_virtual,individuo_map[0],individuo_map[1]])
                req_atendidas +=1
            
        i+=1

    return req_mapeadas,req_atendidas,req_nao_atendidas

def processamento_requisicoes_algoritimo_genetico_paralelo(requisicoes,rd_fisica,req_mapeadas,req_atendidas,req_nao_atendidas):
    
    
    """
        Faz o processamento sequencial das requisicoes 
    """

    i = 1

    for rd_virtual in requisicoes:
        
        print(f"\nRequisicao {i}: ")

        if (rd_virtual.number_of_nodes() > rd_fisica.number_of_edges() or 
            rd_virtual.number_of_nodes() > rd_fisica.number_of_edges()):

            print("\n A rede fisica não é capaz de atender essa requisicao!!!\n A rede virtual possui mais nos ou enlaces que a rede virtual!!\n")
            req_nao_atendidas += 1
        else:

            print("\nProcessando requisicao, aguarde um momento....\n")
            individuo_map = algoritimo_genetico_paralelo(rd_fisica,rd_virtual)

            if individuo_map == []:
                print("\n A rede fisica não é capaz de atender essa requisicao!!!\nNao foi possivel encontrar um mapeamento valido para atender a requisição!!\n")   
                req_nao_atendidas += 1
            else:
                nos_mapeados,enlaces_mapeados = consume_recursos(individuo_map[1],rd_fisica,rd_virtual)
                print("\nIncorporação da rede virtual concluida com sucesso!!")
                print(f"Mapeamento da requisição na Rede Fisica:\n nos:{individuo_map[0]}\n enlaces: {individuo_map[1]}\n")

                req_mapeadas.append([rd_virtual,individuo_map[0],individuo_map[1]])
                req_atendidas +=1
            
        i+=1

    return req_mapeadas,req_atendidas,req_nao_atendidas


def processamento_requisicoes_paralelas(requisicoes,rd_fisica,req_mapeadas,req_atendidas,req_nao_atendidas):

    """
        Faz o processamento paralelo de varias requisicoes ao mesmo tempo
    """

    i = 0
    req_processadas = 0
    num_threads = 4

    threads = []

    while(req_processadas < len(requisicoes)):

        while(i < num_threads and req_processadas < len(requisicoes)):
            
            rd_virtual = requisicoes[req_processadas]

            print(f"\nRequisicao {req_processadas+1}: ")
            print("\nProcessando requisicao, aguarde um momento....\n")

            if (rd_virtual.number_of_nodes() > rd_fisica.number_of_edges() or 
                rd_virtual.number_of_nodes() > rd_fisica.number_of_edges()):

                print("\n A rede fisica não é capaz de atender essa requisicao!!!\n A rede virtual possui mais nos ou enlaces que a rede virtual!!\n")
                req_nao_atendidas += 1
            else:
            
                th = ThreadReturn(target=algoritimo_genetico_paralelo,args=(rd_fisica,rd_virtual,))
                th.start()

                threads.append(th)
                
            i+=1
            req_processadas+= 1 
        
        
        for th in threads:
            individuo_map = th.join()
        
            if individuo_map == []:
                print("\n A rede fisica não é capaz de atender essa requisicao!!!\nNao foi possivel encontrar um mapeamento valido para atender a requisição!!\n")   
                req_nao_atendidas += 1
            else:
                nos_mapeados,enlaces_mapeados = consume_recursos(individuo_map[1],rd_fisica,rd_virtual)
                print("\nIncorporação da rede virtual concluida com sucesso!!")
                print(f"Mapeamento da requisição na Rede Fisica:\n nos:{individuo_map[0]}\n enlaces: {individuo_map[1]}\n")

                req_mapeadas.append([rd_virtual,individuo_map[0],individuo_map[1]])
                req_atendidas +=1
        
        i = 0
        threads = []

    return req_mapeadas,req_atendidas,req_nao_atendidas


def adiciona_recurso_cpu(rd_fisica,no,recurso):

    if rd_fisica.has_node(no):

        rd_fisica.nodes[no]['cpu'] += recurso
    
    else:
        return False

    return True

def adiciona_recurso_enlace(rd_fisica,no1,no2,recurso):

    if rd_fisica.has_edge(no1,no2):

        rd_fisica.get_edge_data(no1,no2)['weight'] += recurso
    
    else:
        return False

    return True






