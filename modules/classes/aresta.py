class Aresta(object):
    """
    Representa uma aresta do dígrafo.
    In:
        origem:Nodo = nodo de origem.
        destinos:Nodo(s) = lista de nodos de destino.
    """
    def __init__(self, origem, destinos):
        self.origem = origem
        self.destinos = list(destinos)

    def __str__(self):
        return 'Origem: ' + str(self.origem) + ' Destinos:' + str(self.destinos)
