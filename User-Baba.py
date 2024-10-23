import IUser;

class Baba(IUser):
    def __init__(self,nome,email,cpf,contato,endereco,avaliacao):
        super().__init__(self,nome,email,cpf,contato,endereco)
        self._avaliacao = avaliacao
        self._certidoes = []

    @property
    def getAvaliacao(self):
        return self._avaliacao
    
    @property
    def getCertidoes(self):
        return self._certidoes

    def addCertidao(self, certidao):
        self._certidoes.append(certidao)

    def rmvCertidao(self, certidao):
        self._certidoes.pop(certidao)
