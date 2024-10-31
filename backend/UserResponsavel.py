import UserInterface as UserInterface;

class Responsavel(UserInterface.IUser):

    def __init__(self, nome, email, cpf, contato, endereco, foto, dataNasc, userId):
        super().__init__(nome, email, cpf, contato, endereco, foto, dataNasc, userId)
        