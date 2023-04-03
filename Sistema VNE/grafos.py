import networkx as nx
from matplotlib import pyplot as plt
import json

def criar_rd_fisica():
    rd_fisica =  nx.Graph()

    rd_fisica.add_nodes_from([

        (0, {"cpu": 60}),(1, {"cpu": 70}),(2, {"cpu": 65}),(3, {"cpu": 70}),
        (4, {"cpu": 65}),(5, {"cpu": 52}),(6, {"cpu": 83}),(7, {"cpu": 99}),
        (8, {"cpu": 88}),(9, {"cpu": 98}),(10, {"cpu": 70}),(11, {"cpu": 50}),

        (12, {"cpu": 88}),(13, {"cpu": 98}),(14, {"cpu": 70}),(15, {"cpu": 50}),
        (16, {"cpu": 50}),(17, {"cpu": 90}),(18, {"cpu": 90}),(19, {"cpu": 95}),

    ])

    rd_fisica.add_weighted_edges_from([
        (0,2,30),(0,3,50),(5,0,60),(2,1,55),(1,4,43),(3,5,70),
        (3,6,70),(5,2,90),(5,1,60),(7,6,60),(5,4,90),(5,6,45),
        (5,7,57),(4,7,66),(6,8,80),(6,9,77),(8,7,39),(7,10,48),
        (3,2,50),(8,10,45),(8,12,45),(10,11,45),(12,9,77),(10,14,70),
        (10,19,75),(8,19,75),(12,19,70),(11,19,85), (3,7,66),(6,12,80),(12,11,77),
        (11,14,39),(10,13,48),(11,10,45),(7,13,45),(4,13,72),(14,13,72),
        (8,13,72),(15,13,75),(14,15,66),(16,15,90),(16,18,80),(14,18,70),
        (15,18,85),(17,18,80),(9,8,72),(17,16,82),(17,14,92),(17,11,62),
        
        ]
    )

    return rd_fisica

def plotar_rede(rd):
    edge_labels = dict([((n1, n2), [rd.get_edge_data(n1,n2)['weight']][0]) for n1, n2 in rd.edges])
    pos = nx.spring_layout(rd)
    plt.figure()

    nx.draw(
        rd, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='blue', alpha=0.9,
        labels={node: node for node in rd.nodes()}
    )
    nx.draw_networkx_edge_labels(
        rd, pos,
        edge_labels=edge_labels,
        font_color='red'
    )


    plt.figure(figsize=(10,6))
    plt.show()


def plotar_rede_incorporada(rd_fisica,nos_mapeados,enlaces_mapeados):
        
    edge_labels = dict([((n1, n2), [rd_fisica.get_edge_data(n1,n2)['weight']][0]) for n1, n2 in rd_fisica.edges])
    pos = nx.spring_layout(rd_fisica)
    plt.figure()

    node_colors = []
    for node in rd_fisica.nodes():
        if node in nos_mapeados:
            node_colors.append('red')
        else:
            node_colors.append('blue')


    edge_colors = []
    for edge in rd_fisica.edges():
        if list(edge) in enlaces_mapeados:
            edge_colors.append('red')
        else:
            edge_colors.append('black')


    nx.draw(
        rd_fisica, pos, edge_color=edge_colors, width=1, linewidths=1,
        node_size=500, node_color=node_colors, alpha=0.9,
        labels={node: node for node in rd_fisica.nodes()}
    )

    nx.draw_networkx_edge_labels(
        rd_fisica, pos,
        edge_labels=edge_labels,
        font_color='black'
    )


    plt.figure(figsize=(10,6))
    plt.show()

def cria_rede_virtual(requsicao):

    try:
        with open(requsicao) as req:
            requsicao = json.load(req)
    except:
        return None
    
    redes = []

    for rq in requsicao.values():

        nos = []
        enlaces = []

        for no,cpu in rq['nos'].items():
            nos.append((int(no),cpu))
        
        for enlace in rq['enlaces'].values():
            enlace = enlace.replace('(','')
            enlace = enlace.replace(')','')
            enlace = enlace.split(",")
            enlaces.append((int(enlace[0]),int(enlace[1]),int(enlace[2])))
        
        rede =  nx.Graph()
        rede.add_nodes_from(nos)
        rede.add_weighted_edges_from(enlaces)

        redes.append(rede)

    return redes


