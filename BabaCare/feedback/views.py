from django.shortcuts import render, redirect, get_object_or_404
from perfis.models import Servico
from .models import Feedback
from .forms import FeedbackForms
from django.contrib import messages

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
    
    servico = Servico.objects.filter(id=contract).first()
    try:
        feedback = Feedback.objects.filter(contract=servico).first()
    except Feedback.DoesNotExist:
        feedback = None
    
    #editar
    if(feedback):
        form = FeedbackForms(data=(request.POST or None), instance = feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Avaliação editada!')
            return redirect('users:servicos_responsavel')
        
        return render(request, 'feedback/give_feedback_page.html', {'form': form, 'contract': servico})
    #primeira avaliação
    else:
        if request.method == 'POST':
            form = FeedbackForms(data=(request.POST or None))
            if form.is_valid():
                aux = form.save(commit=False)
                aux.contract = servico
                form.save()
                return redirect('home')
        else:
            form = FeedbackForms()
        
    return render(request, 'feedback/give_feedback_page.html', {'form': form, 'contract': servico})