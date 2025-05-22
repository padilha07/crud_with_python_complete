from django.shortcuts import render, redirect
from app.forms import AlunosForm
from app.models import Alunos
from django.core.paginator import Paginator

def home(request):
    search = request.GET.get('search')
    serie = request.GET.get('serie')

    alunos = Alunos.objects.all().order_by('id')

    if search:
        alunos = alunos.filter(nome__icontains=search)

    if serie:
        alunos = alunos.filter(serie=serie)

    paginator = Paginator(alunos, 5)
    page = request.GET.get('page')
    alunos_paginated = paginator.get_page(page)

    # pega todas as séries únicas disponíveis
    series_disponiveis = Alunos.objects.values_list('serie', flat=True).distinct().order_by('serie')

    return render(request, 'index.html', {
        'db': alunos_paginated,
        'series': series_disponiveis
    })


def form(request):
    data = {'form': AlunosForm()}
    return render(request, 'form.html', data)

def create(request):
    form = AlunosForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'form.html', {'form': form})

def view(request, pk):
    data = {'db': Alunos.objects.get(pk=pk)}
    return render(request, 'view.html', data)

def edit(request, pk):
    aluno = Alunos.objects.get(pk=pk)
    form = AlunosForm(instance=aluno)
    return render(request, 'form.html', {'form': form, 'db': aluno})

def update(request, pk):
    aluno = Alunos.objects.get(pk=pk)
    form = AlunosForm(request.POST or None, instance=aluno)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'form.html', {'form': form, 'db': aluno})

def delete(request, pk):
    aluno = Alunos.objects.get(pk=pk)
    aluno.delete()
    return redirect('home')
