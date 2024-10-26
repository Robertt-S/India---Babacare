class Avaliacao:
    def __init__(self, nome: str, nota: float, descricao: str):
        self.nome = nome
        self.nota = nota
        self.descricao = descricao
    
#region GETTERS

    @property
    def getNome(self):
        return self.nome
    
    @property
    def getNota(self):
        return self.nota
    
    @property
    def getDescricao(self):
        return self.descricao

#endregion

#region SETTERS

    @property
    def setNota(self, novaNota):
        self.nota = novaNota

    @property
    def setDescricao(self, novaDescricao):
        self.descricao = novaDescricao

#endregion