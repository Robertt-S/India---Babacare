import datetime
#precisa importar annotations para que o Python permita que eu referencie IUser dentro dela própria (faço isso para ter o autor das avaliacoes)
from TypeAvaliacao import Avaliacao

class IUser(): #interface comum

    def __init__(self,nome :str, email: str, cpf: str, contato:str, endereco:str, foto, dataNasc: datetime, userId: int):
        self._nome = nome
        self._email = email
        self._cpf = cpf
        self._contato = contato
        self._endereco = endereco
        self._foto = foto
        self._avaliacao: list[Avaliacao] = []
        self._dataNasc = dataNasc
        self._id = userId
    
#region GETTER DOS ATRIBUTOS

    @property
    def getNome(self):
        return self._nome
    
    @property
    def getEmail(self):
        return self._email
    
    @property
    def getCpf(self):
        return self._cpf
    
    @property
    def getContato(self):
        return self._contato
        
    @property
    def getEndereco(self):
        return self._endereco
    
    @property
    def getFoto(self):
        return self._foto
    
    @property
    def getListaAvaliacao(self):
        return self._avaliacao
    
    @property
    def getDataNascimento(self):
        return self._dataNasc
    
    @property
    def getId(self):
        return self._id
    
    def getAvaliacao(self, id: int):
        for i in self._avaliacao:
            if i.getId == id:
                return i
    
#endregion

#region SETTER DOS ATRIBUTOS MODIFICÁVEIS
    def setEmail(self,novoEmail):
        self._email = novoEmail

    def setContato(self,novoContato):
        self._contato = novoContato

    def setEndereco(self,novoEndereco):
        self._endereco = novoEndereco

    def addAvaliacao(self, novaAvaliacao: Avaliacao):
        for i in self._avaliacao:
            if i.getAutor == novaAvaliacao.autor:
                return -1
        self._avaliacao.append(novaAvaliacao)
        return 0
    #   Uma pessoa pode avaliar um perfil apenas 1 vez, entao se ja houver avaliacao dessa pessoa, 
    #retorna -1 e nao adiciona outra. Senao, retorna 0 e adiciona a avaliacao
    def rmvAvaliacao(self, id: int):
        for i in self._avaliacao:
            if i.getId == id:
                self._avaliacao.remove(i)
                break
  
#endregion
    
    def getUserNota(self):
        if(len(self._avaliacao) == 0):
            return -1
        else:
            count = 0
            sum = 0
            for i in self._avaliacao:
                sum = sum + i.getNota
                count+=1
            return sum/count
    #se for um usuário novo, devolve -1. Senão a média das notas
    
    def getIdade(self):
        today = datetime.datetime.now()
        idade = today.year - self._dataNasc.year
        # se a pessoa já fez aniversário no ano
        if(today.month, today.day) < (self._dataNasc.month, self._dataNasc.day):
            idade -= 1
        
        return idade