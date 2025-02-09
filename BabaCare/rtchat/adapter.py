import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import Message  # Supondo que exista um modelo Message no banco de dados

# Adapter para alternar entre modelos
class Moderador:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.local_models = {
            "unitary/toxic-bert": self.api_hugging,
        }
    
    def api_hugging(self, modelo, msg):
        """
        Envia o texto para o Hugging Face Inference API.
        """
        api_url = f"https://api-inference.huggingface.co/models/{modelo}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"inputs": msg}
        
        resposta = requests.post(api_url, headers=headers, json=payload)
        if resposta.status_code == 200:
            result = resposta.json()
            labels = result[0]
            for label in labels:
                if label['label'] in ["toxic", "insult", "hate", "threat"] and label['score'] > 0.5:
                    return f"Conteúdo inapropriado, reescreva com cuidado: {label['label']} ({label['score']:.2f})"
            return "Mensagem segura."
        else:
            return f"Erro ao acessar API: {resposta.status_code}, {resposta.text}"
    
    def moderar_msg(self, modelo, msg):
        """
        Modera a mensagem com base no modelo escolhido.
        """
        if modelo in self.local_models:
            return self.local_models[modelo](modelo, msg)
        return "Modelo desconhecido ou não suportado."

# View para exibir mensagens e moderação
def message_list(request):
    messages = Message.objects.all()
    moderator = Moderador(api_key="YOUR_HUGGING_FACE_API_KEY")
    for message in messages:
        message.moderation_status = moderator.moderar_msg("unitary/toxic-bert", message.text)
    return render(request, "messages.html", {"messages": messages})

# API para moderação de mensagens
def moderate_api(request):
    if request.method == "POST":
        message_text = request.POST.get("message", "")
        moderator = Moderador(api_key="YOUR_HUGGING_FACE_API_KEY")
        result = moderator.moderar_msg("unitary/toxic-bert", message_text)
        return JsonResponse({"message": message_text, "moderation_result": result})
    return JsonResponse({"error": "Método não permitido"}, status=405)
