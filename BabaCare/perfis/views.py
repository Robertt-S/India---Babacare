from django.shortcuts import render, redirect
#from .models import Perfil_Baba
from users.models import Baba as Perfil_Baba
from users.models import Responsavel as Perfil_Responsavel
from .forms import EditBabaForm, EditRespForm

# Create your views here.

def baba_list(request):
    perfis = Perfil_Baba.objects.all()
    return render(request, 'perfis/baba_list.html', {'perfis': perfis})

# passa o id do perfil também
def edit_page(request, perfil_id):
    isbaba = request.user.isBaba
    if isbaba:
        #vai ver na tabela de perfis e buscar aquela com pk igual a que a gente clica na pagina
        perfil = Perfil_Baba.objects.get(pk=perfil_id)
        #form para editar
        #instance=perfil, na hora de editar, ele mostra o texto que já está gravado no perfil
        form = EditBabaForm(data=(request.POST or None),files=(request.FILES or None), instance = perfil)
    else:
        perfil = Perfil_Responsavel.objects.get(pk=perfil_id)
        form = EditRespForm(data=(request.POST or None),files=(request.FILES or None), instance = perfil)
    if form.is_valid():
        form.save()
        return redirect('perfis:my_page')
    
    return render(request, 'perfis/edit_page.html', {'perfil':perfil, 'form':form})

def my_page(request):
    if request.user.is_authenticated:
        eu_id = request.user.id
        isbaba = request.user.isBaba
        if isbaba: perfil = Perfil_Baba.objects.get(id=eu_id)
        else: perfil= Perfil_Responsavel.objects.get(id=eu_id)
        return render(request,'perfis/own_page.html',{'perfil': perfil,'eu_id':eu_id})
    

def page_baba(request,slug):
    perfilB = Perfil_Baba.objects.get(slug=slug) 
    #{'nome do conjunto de informações': informaçõesPassadas}
    return render(request, 'perfis/baba_page.html', {'perfilBaba': perfilB})

