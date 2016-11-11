class Nodo(object):
    """
    Representa um nodo do dígrafo.

    In:
        nome:string = nome do nodo.
    """
    def __init__(self, nome):
        self.nome = str(nome)

    def __str__(self):
        return self.nome
