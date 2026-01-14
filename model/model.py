from itertools import combinations

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.album_id=[]
        self.album=[]
        self.tracce=[]
        self.pt=[]
        self.album_diz={}
        self.load_tracce()
        self.load_pt()


        self.pt_map={}
        self.node=[]
        self.G=nx.Graph()

    def load_tracce(self):
        self.tracce=DAO.get_tracce()

    def load_pt(self):
        self.pt=DAO.get_p_t()

    def costruisci_map(self):

        for p in self.pt:
            if p[0] not in self.pt_map:
                self.pt_map[p[0]]=set()
                self.pt_map[p[0]].add(self.tracce[p[1]].album_id)

            else:
                self.pt_map[p[0]].add(self.tracce[p[1]].album_id)
        print(self.pt_map)

    def costruisci_grafo(self,soglia):

        self.G.clear()
        self.costruisci_map()
        print("costruisco")
        self.album_id=DAO.get_album_id(soglia)


        self.G.add_nodes_from(self.album_id)
        print(self.album_id)
        for p in self.pt_map.keys():
            print("sono io")
            print(p)
            lista_nodi=[]
            for i in self.pt_map[p]:
                if i in self.album_id:
                    lista_nodi.append(i)
            archi=list(combinations(lista_nodi, 2))
            print(archi)
            self.G.add_edges_from(archi)
        print(self.G)

    def numero_nodi(self):
        return self.G.number_of_nodes()

    def numero_archi(self):
        return self.G.number_of_edges()

    def get_nodes(self):
        return self.G.nodes()

    def get_diz_album(self,soglia):
        self.album_diz=DAO.get_album(soglia)
        return self.album_diz

    def get_connesse(self,nodo):
        componenti=list(nx.node_connected_component(self.G,nodo))
        return componenti

    def get_set(self,album,durata_m):
        self.sol_best=[]
        componenti=self.get_connesse(album)
        durata_corrente=self.album_diz[album].durata/60000
        partial_set=[album]
        self.ricorsione(componenti,partial_set,durata_corrente,durata_m)
        return self.sol_best

    def ricorsione(self,albums,partial_set,durata_corrente,durata_m):
        if len(partial_set)>=len(self.sol_best):
            self.sol_best=partial_set[:]
        for a in albums:
            if a in partial_set:
                continue
            durata_corrente+=self.album_diz[a].durata/60000
            if durata_corrente>durata_m:
                return
            else:
                partial_set.append(a)
                self.ricorsione(albums,partial_set,durata_corrente,durata_m)
                partial_set.pop()





