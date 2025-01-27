from django.shortcuts import render, redirect, get_object_or_404
from perfis.models import Servico
from .models import Feedback
from .forms import FeedbackForms

def feedback_page(request, contract):
    feedback = Feedback.objects.get(contract=contract)
    return render(request, 'feedback/feedback_page.html', {'feedback': feedback})

def give_feedback(request, servico_id):
    contract = get_object_or_404(Servico, id=servico_id, responsavel=request.user)
    
    if Feedback.objects.filter(contract=contract).exists():
        return redirect('users:servicos_finalizados')
    
    if request.method == 'POST':
        form = FeedbackForms(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.contract = contract
            feedback.baba = contract.baba
            feedback.responsavel = contract.responsavel
            feedback.save()
            return redirect('users:servicos_finalizados')
    else:
        form = FeedbackForms()
    
    return render(request, 'feedback/give_feedback_page.html', {'form': form, 'contract': contract})

def edit_feedback(request, contract):
    feedback = Servico.objects.get(id=contract)
    form = FeedbackForms(data=(request.POST or None), instance = feedback)
    if form.is_valid():
        form.save()
        return redirect('home')
    
    return render(request, 'feedback/give_feedback_page.html', {'form': form, 'contract': contract})