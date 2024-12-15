from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages import get_messages
from users.views import cadastro_baba, cadastro_responsavel, login_view
from perfis.views import edit_page
from django.test import TestCase, RequestFactory, Client
from users.models import Baba, Responsavel

class PerfilBabaTests(TestCase):
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

    def test_EditBabaPage(self):
        #As funções SessionMiddleware e MessageMiddleware precisam de um get_response para funcionarem, então criamos esse fake para elas funcionarem
        def get_response(request):
            return None
        
        #Criação de user babá, vide tests.py da users
        request = self.factory.post('/cadastro_baba/', self.baba_data)
        SessionMiddleware(get_response).process_request(request)
        MessageMiddleware(get_response).process_request(request)
        cadastro_baba(request)
        self.assertTrue(Baba.objects.filter(cpf=self.baba_data['cpf']).exists()) #Verificando que a Babá foi realmente criada e está no Banco de Dados
        baba1 = Baba.objects.filter(cpf=self.baba_data['cpf'])[0]

        #Fazendo login de usuário, já que é necessário estar autenticado para fazer as mudanças
        #O cliente também deve ser usado para fazer o post utilizando sua autenticação
        cliente = Client()
        cliente.login(email=baba1.email, password=self.baba_data['senha_1'])

        self.baba_edited = {
            'email': 'fulana_silva@hotmail.com',
            'telefone': '1133334444',
            'endereco': '12460158',
            'bioBaba': 'Experiente',
            'habilidades': 'Muitas',
            'foto': ''
        }
        request = cliente.post('/perfis/edit_page/'+str(baba1.id)+'/', self.baba_edited)
        request.user = baba1
        request.POST = self.baba_edited
        request.FILES = None
        #Como a views neste caso não utiliza as messages do django, não é necessário usar os middlewares
        response = edit_page(request, baba1.id)
        #Atualizar a variável agora que editamos, pegar de novo na base de dados
        baba1 = Baba.objects.filter(cpf=self.baba_data['cpf'])[0]
        self.assertEqual(response.status_code, 302) #Código será 302 pois a views retorna um redirect
        self.assertTrue(response.url.startswith('/perfis/my_page')) #Verificando que o redirect está enviando para o perfil
        self.assertEqual(baba1.email, self.baba_edited['email'])
        self.assertEqual(baba1.telefone, self.baba_edited['telefone'])
        self.assertEqual(baba1.endereco, self.baba_edited['endereco'])
        self.assertEqual(baba1.bioBaba, self.baba_edited['bioBaba'])
        self.assertEqual(baba1.habilidades, self.baba_edited['habilidades'])



        #request = self.factory.post('perfis/edit_page/'+str(baba1.id), self.baba_edited)

        #response = edit_page(request, baba1.id)

        
