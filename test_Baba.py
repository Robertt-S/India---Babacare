from UserBaba import Baba
from TypeAvaliacao import Avaliacao

class TestBaba:  
        name = 'Evandro'
        email = 'ek.kayano@unifesp.br'
        cpf = '098.765.432-10'
        contact = '4002-8922'
        address = 'Av. Cesare Monsueto Giulio Lattes, 1201 - Eugênio de Melo, São José dos Campos - SP, 12247-014'
        photo = 'profile.jpg'
        
        def test_Baba_properties(self):
            babySitter = Baba('Evandro',
                                'ek.kayano@unifesp.br',
                                '098.765.432-10',
                                '4002-8922',
                                'Av. Cesare Monsueto Giulio Lattes, 1201 - Eugênio de Melo, São José dos Campos - SP, 12247-014',
                                'profile.jpg'
                                )
            assert babySitter.getNome == self.name
            assert babySitter.getEmail == self.email
            assert babySitter.getCpf == self.cpf
            assert babySitter.getContato == self.contact
            assert babySitter.getEndereco == self.address
            assert babySitter.getFoto == self.photo

        def test_Baba_Avaliacao(self):

            babySitter = Baba(self.name,self.email,self.cpf,self.contact,self.address,self.photo)
            babySitter.addAvaliacao(Avaliacao(1,'Thiago',0.0,'Péssimo atendimento!'))
            babySitter.addAvaliacao(Avaliacao(2,'Robert',5.0,'Bom Atendimento'))

            assert babySitter.getUserNota() == 2.5
            babySitter.rmvAvaliacao(2)
            assert babySitter.getUserNota() == 0.0
            
        def test_Baba_CertifHabil(self):
            # atributos certificados e habilidades não definidos ainda
            babySitter = Baba(self.name,self.email,self.cpf,self.contact,self.address,self.photo)
            
            babySitter.addCertificado(1)
            babySitter.addCertificado(3)
            babySitter.addCertificado(4)
            babySitter.addHabilidade(2)
            babySitter.addHabilidade(0)
            assert len(babySitter.getCertificados) == 3
            assert len(babySitter.getHabilidades) == 2
            babySitter.rmvCertificado(1)
            babySitter.rmvHabilidade(0)
            assert len(babySitter.getCertificados) == 2
            assert len(babySitter.getHabilidades) == 1