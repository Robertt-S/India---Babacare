import unittest
from TypeAvaliacao import Avaliacao

class TestAvaliacao(unittest.TestCase):
    
    def setUp(self):
        self.avaliacao = Avaliacao(id=1, autor="Isaque", nota=4.5, descricao="Ótimo serviço")

    def test_initialization(self):
        self.assertEqual(self.avaliacao.id, 1)
        self.assertEqual(self.avaliacao.autor, "Isaque")
        self.assertEqual(self.avaliacao.nota, 4.5)
        self.assertEqual(self.avaliacao.descricao, "Ótimo serviço")

    def test_getters(self):
        self.assertEqual(self.avaliacao.getId, 1)
        self.assertEqual(self.avaliacao.getAutor, "Isaque")
        self.assertEqual(self.avaliacao.getNota, 4.5)
        self.assertEqual(self.avaliacao.getDescricao, "Ótimo serviço")

    def test_setNota(self):
        self.avaliacao.setNota = 3.7
        self.assertEqual(self.avaliacao.nota, 3.7)

    def test_setDescricao(self):
        self.avaliacao.setDescricao = "Serviço satisfatório"
        self.assertEqual(self.avaliacao.descricao, "Serviço satisfatório")

if __name__ == '__main__':
    unittest.main()
