# from django.shortcuts import redirect, render

# from rtchat.models import Mensagem
# from users.models import Baba, Responsavel

# # Create your views here.
# def chatPage(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     context = {}
#     return render(request, 'chat.html', context)


# def privateChat(request, baba_id, resp_id):
#     if not request.user.is_authenticated:
#         return redirect('login')
    
#     babaId = Baba.objects.get(id=baba_id)
#     respId = Responsavel.objects.get(id=resp_id)
    
#     mensagens = Mensagem.objects.filter(
#         baba=babaId,
#         responsavel=respId
#     ).order_by('data_envio')
        
#     context = {
#         'mensagens': mensagens,
#         'baba': babaId,
#         'responsavel': respId,
#     }
    
#     return render(request, 'chat.html', context)

from django.shortcuts import redirect, render
from django.http import JsonResponse
from rtchat.models import Mensagem
from users.models import Baba, Responsavel
from .moderador_mensagem import moderate_message  # Importando o moderador

# Página principal do chat
def chatPage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'chat.html')

# Página de chat privado entre Baba e Responsável
def privateChat(request, baba_id, resp_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    baba = Baba.objects.get(id=baba_id)
    responsavel = Responsavel.objects.get(id=resp_id)
    
    mensagens = Mensagem.objects.filter(
        baba=baba,
        responsavel=responsavel
    ).order_by('data_envio')
        
    context = {
        'mensagens': mensagens,
        'baba': baba,
        'responsavel': responsavel,
    }
    
    return render(request, 'chat.html', context)

# API para envio de mensagens
def enviar_mensagem(request):
    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()
        baba_id = request.POST.get("baba_id")
        resp_id = request.POST.get("resp_id")

        # Checar se a mensagem é ofensiva
        resultado_moderacao = moderate_message(texto)
        if "Mensagem inapropriada" in resultado_moderacao:
            return JsonResponse({"erro": resultado_moderacao}, status=400)

        # Criar e salvar a mensagem no banco de dados
        baba = Baba.objects.get(id=baba_id)
        responsavel = Responsavel.objects.get(id=resp_id)
        mensagem = Mensagem.objects.create(
            texto=texto,
            baba=baba,
            responsavel=responsavel
        )

        return JsonResponse({"mensagem": mensagem.texto, "status": "enviado"})

    return JsonResponse({"erro": "Método não permitido"}, status=405)

