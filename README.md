# Projeto India: Babacare


Setup inicial do Django passo a passo, assumindo que git e python ja estejam instalados no windows: 

Pessoal fiz esse passo a passo para todo mundo estar codando no mesmo ambiente pelo vscode então tentem fazer isso já nos proximos dias
para resolvermos qualquer problema de configuração, dependencias etc.

IMPORTANTE: Antes de fazer um git pull, push ou clone novamente siga essas instruções:
Primeiro vamos setar um ambiente virtual, depois instalar e configurar o django e por fim salvar as variaveis de ambiente
(secret keys localmente). Após esse passo a passo vc pode retornar com os push, commits a vontade.  

# Setar Venv:

Abra o vscode como administrador na pasta do babacare

Verifique as versões do python = 3.13.0 e virtual env = 20.27.0 com os comandos:

python --version

virtualenv --version

Idealmente é bom tds estarem com a mesma versão para evitar problemas. 

Executar:

virtualenv venv

venv\Scripts\Activate

Com isso é para aparecer (venv) no terminal e uma nova pasta chamada venv. 

Vc tbm pode conferir se esta  codando na venv com cnrtl + shift + P, digitar python select interpreter e clicar em pyhton venv 3.13.0

OBS: se algm erro de script ocorrer é preciso alterar a politica de execuçaõ de script do windows para unrestricted. Abra o link de ajuda da mensagem de erro se necessario. 

# Instalar django: 

python.exe -m pip install --upgrade pip

pip install django 

pip install python-dotenv

django-admin startproject setup .  
(Com o ponto final após setup)

Alterando o timezone para brasil:

setup/settings.py na linha 106 trocar por: 

pt-br

e no timezone trocar UTC por:

America/Sao_Paulo


# Variaveis de ambiente .env :

Agora o mais importante é salvar sua secret key,

Criar arquivo .env (fora de tudo)

Copiar sua secret key (sem as aspas duplas) proximo a linha 25 em setup/settings.py

colar secret key sem aspas no arquivo .env criado da seguinte forma: SECRET_KEY = sua_secret_key_aqui

salve a sua .env, ela não é enviada ao github

execute então um pull:

git pull origin main

E pronto é para tudo estar correto.
See quiser testar o servidor execute: python manage.py runserver
Doc Oficial do django: https://www.djangoproject.com/start/overview/