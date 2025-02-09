import sys
import threading
from django.apps import AppConfig

class PerfisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'perfis'

    def ready(self):
        # Only trigger on `runserver`
        if 'runserver' in sys.argv:
            threading.Thread(target=self.baba_match).start()

    def baba_match(self):
        """ Importa-se as bibliotecas aqui para evitar problemas de não carregamento de módulos """
        from users.models import Baba, Responsavel
        from contrato.views import SentenceSimilarityAdapter

        nome_modelo = "sentence-transformers/all-MiniLM-L6-v2"
        sentence_similarity_model = SentenceSimilarityAdapter(nome_modelo, use_api=True)

        babas = Baba.objects.all()
        responsaveis = Responsavel.objects.all()

        responsavel_bio = ""
        babas_bios = []
        taxas_similaridades_babas = {}


        ## Checa se é necessário atualizar a similaridade de babas
        for responsavel in responsaveis:
            if len(responsavel.babasSimilares) == len(babas):
                responsaveis = responsaveis.exclude(id=responsavel.id)
            else:
                pass
        

        if responsaveis:
            for baba in babas:
                babas_bios.append(baba.bioBaba)


        for responsavel in responsaveis:
            responsavel_bio = responsavel.bioResp
            
            if babas_bios:
                similaridades = sentence_similarity_model.sentence_similarity(responsavel_bio, babas_bios)

                for baba in babas:
                    taxas_similaridades_babas[baba.id] = similaridades[babas_bios.index(baba.bioBaba)]
                    
                responsavel.babasSimilares = taxas_similaridades_babas
                responsavel.save()

                taxas_similaridades_babas.clear()
        
        print("Rotina de atualização de similaridade de babás finalizada.")