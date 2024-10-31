import UserInterface as UserInterface;

class Baba(UserInterface.IUser):
    def __init__(self,nome,email,cpf,contato,endereco,foto, dataNasc, userId):
        super().__init__(nome,email,cpf,contato,endereco,foto, dataNasc, userId)
        self._certificados = []
        self._habilidades = []

    @property
    def getCertificados(self):
        return self._certificados
    
    @property
    def getHabilidades(self):
        return self._habilidades


    def addCertificado(self, certificados):
        self._certificados.append(certificados)

    def rmvCertificado(self, certificados):
        self._certificados.pop(certificados)
        
    def addHabilidade(self, habilidades):
        self._habilidades.append(habilidades)

    def rmvHabilidade(self, habilidades):
        self._habilidades.pop(habilidades)
