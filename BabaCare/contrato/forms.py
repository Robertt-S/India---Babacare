from django import forms
import datetime

class ContratacaoForm(forms.Form):
    PERIODOS = [
        ('manhã', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ]
    data_servico = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',  # Faz o HTML renderizar um calendário
                'class': 'form-control calendario-input',
                'min': datetime.date.today().strftime('%Y-%m-%d')  # Impede datas passadas
            }
        ),
        required=True,
        input_formats=['%Y-%m-%d'],  # Aceita o formato do HTML5
        initial=datetime.date.today  # Define a data inicial como hoje
    )

    # periodo = forms.ChoiceField(choices=PERIODOS, required=True)  # Campo obrigatório para selecionar o período
    periodo = forms.ChoiceField(
        choices=PERIODOS,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control periodo-selecao'})
    )