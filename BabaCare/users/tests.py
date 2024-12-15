from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages import get_messages
from django.contrib.auth.hashers import check_password
from django.test import TestCase, RequestFactory
from users.models import Baba, Responsavel
import users.views as views

#Como os testes rodam independentes entre si, todos os testes precisam criar o usuário antes de poder mexer com ele

class BabaTests(TestCase):
    #setUp são os primeiros passos que o teste faz antes de realizar todos os outros testes
    #Neste caso, já criei os dados da babá fictícia aqui
    #RequestFactory precisamos para emular requests nos testes automatizados
    def setUp(self):
        self.factory = RequestFactory()
        self.baba_data = {
            'nome_cadastro': 'Fulana da Silva',
            'email': 'fulana_silva@gmail.com',
            'senha_1': 'fulana@123',
            'senha_2': 'fulana@123',
            'telefone': '1122223333',
            'endereco': '12223430',
            'numero': '1031',
            'nascimento': '1990-10-28',
            'cpf': '45317828791'
        }
    
    def test_BabaCreate(self):

        #As funções SessionMiddleware e MessageMiddleware precisam de um get_response para funcionarem, então criamos esse fake para elas funcionarem
        def get_response(request):
            return None

        #POST no cadastro_baba enviando os dados de formulário preparados acima, para a criação do usuário babá
        request = self.factory.post('/cadastro_baba/', self.baba_data)
        #Precisamos especificar esses middlewares nos testes pois os testes automatizados do django não possuem suporte nativo aos middleware.
        #Sem isso, como usamos mensagens na views.py, ele daria problema.
        SessionMiddleware(get_response).process_request(request)
        MessageMiddleware(get_response).process_request(request)
        response = views.cadastro_baba(request)
        self.assertEqual(response.status_code, 302) #Código será 302 pois a views retorna um redirect
        self.assertTrue(response.url.startswith('/login')) #Verificando que o redirect está enviando para login
        self.assertTrue(Baba.objects.filter(cpf=self.baba_data['cpf']).exists()) #Verificando que a Babá foi realmente criada e está no Banco de Dados
        messages = list(get_messages(request)) #Criando uma lista de mensagens recebidas
        self.assertEqual(str(messages[0]), "Cadastro efetuado com sucesso!") #Verificando que a mensagem recebida foi a correta
    
    def test_BabaDBDataCorrect(self):
        #Criamos o usuário e encontramos ele
        def get_response(request):
            return None
        request = self.factory.post('/cadastro_baba/', self.baba_data)
        SessionMiddleware(get_response).process_request(request)
        MessageMiddleware(get_response).process_request(request)
        views.cadastro_baba(request)
        baba1 = Baba.objects.filter(cpf=self.baba_data['cpf'])[0]
        #Teste para ver se a senha está hasheada no BD
        self.assertTrue(check_password(self.baba_data['senha_1'], baba1.password))
        #Verificando que o booleano indica corretamente que é babá
        self.assertTrue(baba1.isBaba)
        #Verificando que o slug está corretamente usando nome e id
        nomeSlug = self.baba_data['nome_cadastro'].lower()
        nomeSlug = nomeSlug.replace(' ', '-')
        slug = nomeSlug+'-'+str(baba1.id)
        self.assertEqual(baba1.slug, slug)

class RespTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.resp_data = {
            'nome_cadastro': 'Fulano da Silva',
            'email': 'fulano_silva@gmail.com',
            'senha_1': 'fulano@123',
            'senha_2': 'fulano@123',
            'telefone': '1133334444',
            'endereco': '12223430',
            'numero': '1031',
            'nascimento': '1990-10-28',
            'cpf': '07068093868'
        }
    
    def test_RespCreate(self):
        def get_response(request):
            return None

        request = self.factory.post('/cadastro_responsavel/', self.resp_data)
        SessionMiddleware(get_response).process_request(request)
        MessageMiddleware(get_response).process_request(request)
        response = views.cadastro_responsavel(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))
        self.assertTrue(Responsavel.objects.filter(cpf=self.resp_data['cpf']).exists())
        messages = list(get_messages(request))
        self.assertEqual(str(messages[0]), "Cadastro efetuado com sucesso!")

    def test_RespDBDataCorrect(self):
        #Criamos o usuário e encontramos ele
        def get_response(request):
            return None
        request = self.factory.post('/cadastro_responsavel/', self.resp_data)
        SessionMiddleware(get_response).process_request(request)
        MessageMiddleware(get_response).process_request(request)
        views.cadastro_responsavel(request)
        resp1 = Responsavel.objects.filter(cpf=self.resp_data['cpf'])[0]
        #Teste para ver se a senha está hasheada no BD
        self.assertTrue(check_password(self.resp_data['senha_1'], resp1.password))
        #Verificando que o booleano indica corretamente que é responsável
        self.assertFalse(resp1.isBaba)
        #Verificando que o slug está corretamente usando nome e id
        nomeSlug = self.resp_data['nome_cadastro'].lower()
        nomeSlug = nomeSlug.replace(' ', '-')
        slug = nomeSlug+'-'+str(resp1.id)
        self.assertEqual(resp1.slug, slug)