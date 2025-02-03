from django.shortcuts import redirect, render

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
    context = {'baba':babaId,'resp': respId}
    return render(request, 'chat.html', context)
