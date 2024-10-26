import users.UserInterface as UserInterface;
from ..types.TypeAvaliacao import Avaliacao

class Responsavel(UserInterface.IUser):


    def __init__(self, nome, email, cpf, contato, endereco, foto):
        super().__init__(nome, email, cpf, contato, endereco, foto)
        self._avaliacao: list[Avaliacao] = []

    @property
    def getAvaliacao(self):
        return self._avaliacao

    def addAvaliacao(self, novaAvaliacao: Avaliacao):
        self._avaliacao.append(novaAvaliacao)

    def rmvAvaliacao(self, nomeAvaliacao):
        for i in self._avaliacao:
            if i.getNome(i) == nomeAvaliacao:
                self._avaliacao.remove(i)
                break