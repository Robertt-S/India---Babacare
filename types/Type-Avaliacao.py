class Avaliacao:
    def __init__(self, nome: str, avaliacao: float, descricao: str):
        self.nome = nome
        self.avaliacao = avaliacao
        self.descricao = descricao
    
#region GETTERS

    @property
    def getNome(self):
        return self.nome
    
    @property
    def getAvaliacao(self):
        return self.avaliacao
    
    @property
    def getDescricao(self):
        return self.descricao

#endregion

#region SETTERS

    @property
    def setAvaliacao(self, novaAvaliacao):
        self.avaliacao = novaAvaliacao

    @property
    def setDescricao(self, novaDescricao):
        self.descricao = novaDescricao

#endregion