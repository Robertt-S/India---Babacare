class Avaliacao:
    def __init__(self, id: int, autor: str, nota: float, descricao: str):
        self.id = id
        self.autor = autor
        self.nota = nota
        self.descricao = descricao
    
#region GETTERS

    @property
    def getId(self):
        return self.id

    @property
    def getAutor(self):
        return self.autor
    
    @property
    def getNota(self):
        return self.nota
    
    @property
    def getDescricao(self):
        return self.descricao

#endregion

#region SETTERS

    def setNota(self, novaNota):
        self.nota = novaNota

    def setDescricao(self, novaDescricao):
        self.descricao = novaDescricao

#endregion