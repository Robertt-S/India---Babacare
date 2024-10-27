from ..users.UserInterface import IUser

class Avaliacao:
    def __init__(self, autor: IUser, nota: float, descricao: str):
        self.autor = autor
        self.nota = nota
        self.descricao = descricao
    
#region GETTERS

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

    @property
    def setNota(self, novaNota):
        self.nota = novaNota

    @property
    def setDescricao(self, novaDescricao):
        self.descricao = novaDescricao

#endregion