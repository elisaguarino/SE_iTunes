import flet as ft
from UI.view import View
from database.dao import DAO
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.album_diz={}
        self.album_selezionato=None

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            soglia=float(self._view.txt_durata.value)
        except:
            self._view.show_alert("inserire un valore valido per i minuti")
            return
        self._model.costruisci_grafo(soglia)
        self._view.lista_visualizzazione_1.controls.clear()
        n_nodi = self._model.numero_nodi()
        n_archi = self._model.numero_archi()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"numero album: {n_nodi} numero archi:{n_archi}"))
        self.popola_dd(soglia)
        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """
        valore = e.control.value
        self.album_selezionato =  int(valore)


    def popola_dd(self, soglia):

        self.album_diz=self._model.get_diz_album(soglia)
        node=self._model.get_nodes()
        for n in node:
            self._view.dd_album.options.append(ft.dropdown.Option(key=n,text=self.album_diz[n].title))
        self._view.update()


    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        if self.album_selezionato is None:
            self._view.show_alert("selezionare un album")
            return
        componenti=self._model.get_connesse(self.album_selezionato)
        num_componenti=len(componenti)
        tot=0
        for a in componenti:
            tot+= self.album_diz[a].durata /60000
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensione componente: {num_componenti}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"durata totale: {tot:.2f}"))
        self._view.update()


    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        try:
            durata_tot=float(self._view.txt_durata_totale.value)
        except:
            self._view.show_alert("inserire un valore valido per i minuti")
            return
        album=self._model.get_set(self.album_selezionato,durata_tot)
        self._view.lista_visualizzazione_3.controls.clear()
        num=len(album)
        tot=0
        for a in album:
            tot+=self.album_diz[a].durata /60000
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"set trovato({num} album, durata: {tot:.2f} minuti)"))
        for a in album:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"-{self.album_diz[a].title} ({self.album_diz[a].durata/60000:.2f}minuti) "))
        self._view.update()
