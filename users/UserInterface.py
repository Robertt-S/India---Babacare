class IUser(): #interface comum
    def __init__(self,nome :str,email: str,cpf: str,contato:str,endereco:str,foto):
        self._nome = nome
        self._email = email
        self._cpf = cpf
        self._contato = contato
        self._endereco = endereco
        self._foto = foto

#region GETTER DOS ATRIBUTOS

    @property
    def getNome(self):
        return self._nome
    
    @property
    def getEmail(self):
        return self._email
    
    @property
    def getCpf(self):
        return self._cpf;
    
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

#endregion
    
