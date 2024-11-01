from abc import ABC, abstractmethod
from typing import Any, Optional
from validdocbr import validdocbr

class RegisterHandler(ABC):
    _next_handler: Optional[Handler]= None

    def set_next(self, handler: Handler) -> Handler:
        #def o proximo handler na cadeia
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Any) -> Optional[str]:
        #passa para o proximo
        if self._next_handler:
            return self._next_handler.handle(request)
        return None

#ta pronto!
class VerifyLegalAge(Handler):
    def handle(self, request: Any) -> Optional[str]:
        if request.get("idade", 0) >= 18:
            #ele valida e passa para prox verificação, se tiver, se for ultimo volta None= aprovado em tds as verificações
            return super().handle(request) 
        else:
            #a ideia é retornar essa mensagem pro usuario, dando print({return}) e para sabermos onde falhou
            return "Falha na verificação: Idade não aprovada!" 


#nao ta pronto, só a estrutura e rascunho
class VerifyDocuments(Handler):
    def handle(self, request: Any) -> Optional[str]:
        if request.get("documentos_validos", False):
            #print("Documentos verificados com sucesso.")
            return super().handle(request)
        else:
            return "Falha na verificação: CPF Inválido!"


#nao ta pronto, só a estrutura e rascunho
class VerifyEmail(Handler):
    def handle(self, request: Any) -> Optional[str]:
        if request.get("email_valido", False):
            return super().handle(request)
        else:
            return "Verificação falhou em: E-mail"



