from django.shortcuts import redirect, render

from rtchat.models import Mensagem
from users.models import Baba, Responsavel

# Create your views here.
def chatPage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    return render(request, 'chat.html', context)


def privateChat(request, baba_id, resp_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    babaId = Baba.objects.get(id=baba_id)
    respId = Responsavel.objects.get(id=resp_id)
    
    mensagens = Mensagem.objects.filter(
        baba=babaId,
        responsavel=respId
    ).order_by('data_envio')
        
    context = {
        'mensagens': mensagens,
        'baba': babaId,
        'responsavel': respId,
    }
    
    return render(request, 'chat.html', context)
