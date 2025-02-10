import random, math
from math import radians, sin, cos, acos
from django.core.management.base import BaseCommand
from users.models import Baba, Responsavel

class Command(BaseCommand):
    help = "Cria 10 perfis de Baba e 2 de Responsavel aleatórios para simulação"


    def handle(self, *args, **options):
            ###--- Dados dos Responsáveis ---###

        lista_responsaveis_bios = [
            "Meu nome é Mariana, sou uma profissional da área de tecnologia, atuando como gerente de projetos em uma multinacional. Tenho uma rotina intensa e viajo ocasionalmente a trabalho. Por isso, busco uma babá responsável, confiável e proativa para cuidar do meu filho de 3 anos. É importante que a profissional tenha experiência com atividades educativas, seja paciente e possa ajudar na organização da rotina dele, incluindo alimentação saudável e brincadeiras estimulantes. Valorizo uma comunicação clara e um ambiente harmonioso em casa.",
            "Sou Pedro, artista visual e freelancer, com uma rotina de trabalho flexível, muitas vezes em casa. Tenho uma filha de 5 anos, cheia de energia e imaginação. Procuro uma babá que seja criativa, carinhosa e com espírito aventureiro para acompanhar nossas jornadas criativas, como atividades ao ar livre, pintura e leitura de histórias. Não busco rigidez, mas sim alguém que saiba incentivar o desenvolvimento dela de maneira leve e divertida. Ter afinidade com artes e música seria um diferencial!"
        ]

        lista_responsaveis_nomes = [
            "Mariana", 
            "Pedro"
        ]

        lista_responsaveis_cpfs = [
            25684826059,
            38816634014
        ]

        lista_responsaveis_nascimentos = [
            "1990-01-01",
            "1985-02-02"
        ]

        lista_responsaveis_emails = [
            "mariana@gmail.com",
            "pedro@gmail.com"
        ]

        lista_responsaveis_telefones = [
            "1",
            "2"
        ]

        lista_responsaveis_enderecos = [
            "Rua A",
            "Rua B"
        ]

        lista_responsaveis_numeros = [
            "1",
            "2"
        ]

        lista_responsaveis_lat_long = [
            [-23.569874, -46.534370],
            [-23.613383, -46.552538]
        ]




        ###--- Dados das Babás ---###

        lista_babas_bios = [
            "Tenho mais de 10 anos de experiência como babá, sempre trabalhando com famílias que valorizam rotina e disciplina. Sou organizada, responsável e sei lidar bem com crianças pequenas, incluindo atividades educativas e cuidados diários. Ideal para um perfil executivo que busca estabilidade e segurança.",
            "Atualmente cursando Pedagogia, adoro aplicar métodos educativos lúdicos que estimulam a curiosidade e o aprendizado das crianças. Sou criativa e flexível, adaptando as atividades conforme o perfil da família. Perfeita para pais que buscam educação leve e divertida.",
            "Falo inglês e francês fluentes, com anos de experiência como babá em diferentes países. Amo introduzir novas culturas às crianças por meio de histórias e músicas. Adequada para famílias globais e pais com rotinas internacionais.",
            "Com formação em artes visuais, trago criatividade para o cuidado com crianças. Gosto de envolver as crianças em atividades artísticas e passeios ao ar livre. Sou perfeita para pais como Pedro, que buscam estímulo artístico para seus filhos.",
            "Tenho especialização em desenvolvimento infantil e experiência com crianças em fase de desenvolvimento emocional. Sou paciente e atenciosa, focando em criar um ambiente seguro e acolhedor. Ideal para perfis preocupados com o bem-estar emocional dos pequenos.",
            "Sou babá profissional e também empreendedora de uma pequena empresa de cuidados infantis. Entendo a necessidade de famílias executivas em busca de rotina, disciplina e cuidados impecáveis. Adequada para mães executivas como Mariana.",
            "Adoro atividades ao ar livre, alimentação saudável e práticas de mindfulness para crianças. Acredito que a tranquilidade e o contato com a natureza ajudam a desenvolver crianças felizes e saudáveis. Ideal para famílias que buscam um estilo de vida natural e equilibrado.",
            "Trabalho com suporte noturno para recém-nascidos e crianças pequenas. Tenho vasta experiência em organização do sono infantil. Uma excelente opção para pais com rotina intensa e que precisam de descanso.",
            "Tenho experiência com esportes infantis e adoro inventar brincadeiras físicas. Perfeita para pais que querem estimular o lado físico e social das crianças, saindo da monotonia.",
            "Apaixonada por tecnologia e educação digital, gosto de ensinar crianças a usarem ferramentas educacionais com responsabilidade. Ideal para pais que apreciam inovação e aprendizado digital."
        ]

        lista_babas_nomes = [
            "Ana",
            "Beatriz",
            "Carla",
            "Daniela",
            "Eliane",
            "Fernanda",
            "Gabriela",
            "Helena",
            "Isabela",
            "Juliana"
        ]

        lista_babas_cpfs = [
            99784491087,
            14181156060,
            53373257018,
            23358827089,
            80177838094,
            58445461052,
            39824471006,
            80028859022,
            18778549051,
            77647232070
        ]

        lista_babas_nascimentos = [
            "1990-01-01",
            "1985-02-02",
            "1980-03-03",
            "1975-04-04",
            "1970-05-05",
            "1965-06-06",
            "1960-07-07",
            "1955-08-08",
            "1950-09-09",
            "1945-10-10"
        ]

        lista_babas_emails = [
            "ana@gmail.com",
            "beatriz@gmail.com",
            "carla@gmail.com",
            "daniela@gmail.com",
            "eliane@gmail.com",
            "fernanda@gmail.com",
            "gabriela@gmail.com",
            "helena@gmail.com",
            "isabela@gmail.com",
            "juliana@gmail.com"
        ]

        lista_babas_telefones = [
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12"
        ]

        lista_babas_enderecos = [
            "Rua C",
            "Rua D",
            "Rua E",
            "Rua F",
            "Rua G",
            "Rua H",
            "Rua I",
            "Rua J",
            "Rua K",
            "Rua L"
        ]

        lista_babas_numeros = [
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12"
        ]

        lista_babas_lat_long = [
            [-23.558491, -46.489069],
            [-23.606940, -46.507424],
            [-23.560234, -46.510927],
            [-23.548695, -46.507495],
            [-23.611378, -46.485569],
            [-23.658591, -46.507911],
            [-23.648261, -46.596366],
            [-23.624649, -46.509139],
            [-23.658521, -46.573266],
            [-23.614693, -46.574764]
        ]

        for i in range(10):
            baba = Baba.objects.create_user(
                nome = lista_babas_nomes[i],
                cpf = lista_babas_cpfs[i],
                nascimento = lista_babas_nascimentos[i],
                email = lista_babas_emails[i],
                telefone = lista_babas_telefones[i],
                endereco = lista_babas_enderecos[i],
                numero = lista_babas_numeros[i],
                password = "teste123",
            )

            baba.bioBaba = lista_babas_bios[i]
            baba.habilidades = ""
            baba.rangeTrabalho = 100
            baba.lat = lista_babas_lat_long[i][0]
            baba.long = lista_babas_lat_long[i][1]
            baba.isBaba = True
            baba.save()

        for i in range(2):
            responsavel = Responsavel.objects.create_user(
                nome = lista_responsaveis_nomes[i],
                cpf = lista_responsaveis_cpfs[i],
                nascimento = lista_responsaveis_nascimentos[i],
                email = lista_responsaveis_emails[i],
                telefone = lista_responsaveis_telefones[i],
                endereco = lista_responsaveis_enderecos[i],
                numero = lista_responsaveis_numeros[i],
                password = "teste123"
            )

            responsavel.bioResp = lista_responsaveis_bios[i]
            responsavel.lat = lista_responsaveis_lat_long[i][0]
            responsavel.long = lista_responsaveis_lat_long[i][1]
            responsavel.isBaba = False
            responsavel.save()

        self.stdout.write(self.style.SUCCESS("Perfis criados com sucesso!"))