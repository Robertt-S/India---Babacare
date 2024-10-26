from ..types.TypeAvaliacao import Avaliacao

class IUser(): #interface comum
    def __init__(self,nome :str,email: str,cpf: str,contato:str,endereco:str,foto):
        self._nome = nome
        self._email = email
        self._cpf = cpf
        self._contato = contato
        self._endereco = endereco
        self._foto = foto
        self._avaliacao: list[Avaliacao] = [] 

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
    
    
    
#endregion

#region SETTER DOS ATRIBUTOS MODIFICÁVEIS
    def setEmail(self,novoEmail):
        self._email = novoEmail

    def setContato(self,novoContato):
        self._contato = novoContato

    def setEndereco(self,novoEndereco):
        self._endereco = novoEndereco

    def addAvaliacao(self, novaAvaliacao: Avaliacao):
        self._avaliacao.append(novaAvaliacao)

    def rmvAvaliacao(self, nomeAvaliacao):
        for i in self._avaliacao:
            if i.getNome(i) == nomeAvaliacao:
                self._avaliacao.remove(i)
                break
            
    def getUserNota(self):
        if(len(self._avaliacao) == 0):
            return -1
        else:
            count = 0
            sum = 0
            for i in self._avaliacao:
                sum = sum + i.getNota()
                count+=1
            return sum/count
    #se for um usuário novo, devolve -1. Senão a média das notas
    
#endregion
    
