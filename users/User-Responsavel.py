import users.UserInterface as UserInterface;

class Responsavel(UserInterface.IUser):

    avaliacao = []

    def __init__(self, nome, email, cpf, contato, endereco, foto):
        super().__init__(nome, email, cpf, contato, endereco, foto)

    @property
    def getAvaliacao(self):
        return self.avaliacao
