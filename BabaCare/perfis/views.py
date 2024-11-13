from django.shortcuts import render, redirect
from .models import Perfil_Baba
from .forms import EditProfileForm

# Create your views here.

def baba_list(request):
    perfils = Perfil_Baba.objects.all() 
    return render(request, 'perfis/baba_list.html', {'perfis': perfils})

# passa o id do perfil também
def edit_page(request, perfil_id):
    #vai ver na tabela de perfis e buscar aquela com pk igual a que a gente clica na pagina
    perfil = Perfil_Baba.objects.get(pk=perfil_id)
    #form para editar
    #instance=perfil, na hora de editar, ele mostra o texto que já está gravado no perfil
    form = EditProfileForm(data=(request.POST or None),files=(request.FILES or None), instance = perfil)
    if form.is_valid():
        form.save()
        return redirect('perfis:my_page')
    
    return render(request, 'perfis/edit_page.html', {'perfil':perfil, 'form':form})

def my_page(request):
    if request.user.is_authenticated:
        eu = request.user
        perfil = Perfil_Baba.objects.get(owner=eu.id) 
        return render(request,'perfis/own_page.html',{'perfil': perfil,'eu':eu})

def page_baba(request,slug):
    perfilB = Perfil_Baba.objects.get(slug=slug) 
    #{'nome do conjunto de informações': informaçõesPassadas}
    return render(request, 'perfis/baba_page.html', {'perfilBaba': perfilB})

