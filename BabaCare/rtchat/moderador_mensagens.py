import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import Message  # Supondo que exista um modelo Message no banco de dados

# Configurar a chave da API
API_URL = "https://api-inference.huggingface.co/models/unitary/toxic-bert"
HEADERS = {"Authorization": f"Bearer YOUR_HUGGING_FACE_API_KEY"}

# Função para moderar mensagens
def moderate_message(message):
    payload = {"inputs": message}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        labels = result[0]
        for label in labels:
            if label['label'] in ["toxic", "insult", "hate", "threat"] and label['score'] > 0.5:
                return f"Mensagem inapropriada detectada: {label['label']} ({label['score']:.2f})"
        return "Mensagem aprovada."
    else:
        return f"Erro: {response.status_code}, {response.text}"

# View para exibir mensagens e moderação
def message_list(request):
    messages = Message.objects.all()
    for message in messages:
        message.moderation_status = moderate_message(message.text)
    return render(request, "messages.html", {"messages": messages})

# API para moderação de mensagens
def moderate_api(request):
    if request.method == "POST":
        message_text = request.POST.get("message", "")
        result = moderate_message(message_text)
        return JsonResponse({"message": message_text, "moderation_result": result})
    return JsonResponse({"error": "Método não permitido"}, status=405)
