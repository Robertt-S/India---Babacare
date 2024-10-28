from UserResponsavel import Responsavel
from TypeAvaliacao import Avaliacao
import datetime

class TestResp:

    nome = "Thiago"
    email = "thiago.capuano@unifesp.br"
    cpf = "123.456.789-69"
    contato = "4002-8922"
    endereco = "Rua dos Bobos, 0"
    dataNascimento = datetime.date(2002,7,11)
    userId = 1

    def test_Resp_confirmBasicData(self):
        Resp = Responsavel("Thiago", "thiago.capuano@unifesp.br", "123.456.789-69", "4002-8922", "Rua dos Bobos, 0", None,"2002-07-11",1)
        assert Resp.getNome == self.nome
        assert Resp.getEmail == self.email
        assert Resp.getCpf == self.cpf
        assert Resp.getContato == self.contato
        assert Resp.getEndereco == self.endereco
        assert Resp.getDataNascimento == self.dataNascimento.strftime("%Y-%m-%d")
        assert Resp.getId == self.userId

    def test_Resp_confirmAvaliacao(self):
        Resp = Responsavel(self.nome, self.email, self.cpf, self.contato, self.endereco, None, self.dataNascimento, self.userId)
        Av = Avaliacao(1, "João", 10, "Muito bom")
        Resp.addAvaliacao(Av)
        assert Resp.getAvaliacao(1) == Av

    def test_Resp_confirmAvaliacaoRmv(self):
        Resp = Responsavel(self.nome, self.email, self.cpf, self.contato, self.endereco, None, self.dataNascimento, self.userId)
        Av = Avaliacao(1, "João", 10, "Muito bom")
        Resp.addAvaliacao(Av)
        assert Resp.getAvaliacao(1) == Av
        Resp.rmvAvaliacao(1)
        assert Resp.getListaAvaliacao == []

    def test_Resp_confirmNota(self):
        Resp = Responsavel(self.nome, self.email, self.cpf, self.contato, self.endereco, None, self.dataNascimento, self.userId)
        Av1 = Avaliacao(1, "João", 10, "Muito bom")
        Av2 = Avaliacao(2, "Maria", 0, "Horrível")
        Resp.addAvaliacao(Av1)
        Resp.addAvaliacao(Av2)
        assert Resp.getAvaliacao(1) == Av1
        assert Resp.getAvaliacao(2) == Av2
        assert Resp.getUserNota() == 5
