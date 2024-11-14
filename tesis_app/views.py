from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, ExamenForm, PerfilForm
from .models import Examen
from django.contrib.auth.forms import AuthenticationForm

import os
import time
import joblib
import pandas as pd
from django.contrib import messages



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('perfil')  # Cambia 'home' por la vista a la que desees redirigir
    else:
        form = AuthenticationForm()

    return render(request, 'tesis_app/login.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Cambia 'home' a la vista deseada
    else:
        form = RegisterForm()
    return render(request, 'tesis_app/register.html', {'form': form})



# def prediagnostico(request):
#     if request.method == 'POST':
#         form = ExamenForm(request.POST)
#         if form.is_valid():
#             examen = form.save(commit=False)
#             examen.user = request.user
#             examen.save()
#             return redirect('historial')
#     else:
#         form = ExamenForm()
#     return render(request, 'tesis_app/prediagnostico.html', {'form': form})

def prediagnostico(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)

        if form.is_valid():
            # Crear una nueva instancia de Examen sin guardar todavía
            examen = form.save(commit=False)
            examen.user = request.user  # Asignar el usuario automáticamente

            # Asignar la fecha de inicio de síntomas
            examen.fsintomas = form.cleaned_data.get('fsintomas')

            # Recopilar datos de síntomas como booleanos
            examen.fiebre = form.cleaned_data.get('fiebre', False)
            examen.dolor_articulaciones = form.cleaned_data.get('dolor_articulaciones', False)
            examen.dolor_detras_de_ojos = form.cleaned_data.get('dolor_detras_de_ojos', False)
            examen.dolor_muscular = form.cleaned_data.get('dolor_muscular', False)
            examen.dolor_de_cabeza = form.cleaned_data.get('dolor_de_cabeza', False)
            examen.erupcion_cutanea = form.cleaned_data.get('erupcion_cutanea', False)
            examen.nauseas_vomitos = form.cleaned_data.get('nauseas_vomitos', False)
            examen.dolor_abdominal_intenso = form.cleaned_data.get('dolor_abdominal_intenso', False)
            examen.vomitos_persistentes = form.cleaned_data.get('vomitos_persistentes', False)
            examen.sangrado_mucosas_y_encias = form.cleaned_data.get('sangrado_mucosas_y_encias', False)
            examen.somnolencia_irritabilidad = form.cleaned_data.get('somnolencia_irritabilidad', False)
            examen.decaimiento = form.cleaned_data.get('decaimiento', False)

            # Guardar el campo 'otros'
            examen.otros = form.cleaned_data.get('otros', '')

            # Obtener el tiempo de detección desde el formulario
            examen.tiempo_deteccion = request.POST.get('tiempo_deteccion', 0)

            # Preparar los datos para la predicción
            datos = [
                examen.fiebre,
                examen.dolor_articulaciones,
                examen.dolor_detras_de_ojos,
                examen.dolor_muscular,
                examen.dolor_de_cabeza,
                examen.erupcion_cutanea,
                examen.nauseas_vomitos,
                examen.dolor_abdominal_intenso,
                examen.vomitos_persistentes,
                examen.sangrado_mucosas_y_encias,
                examen.somnolencia_irritabilidad,
                examen.decaimiento,
            ]

            # Cargar el modelo
            current_dir = os.path.dirname(__file__)
            modelo_path = os.path.join(current_dir, 'models', 'modelo_bosque_aleatorio.pkl')

            try:
                modelo = joblib.load(modelo_path)
            except FileNotFoundError:
                messages.error(request, 'Modelo no encontrado. Asegúrate de que el archivo exista.')
                return render(request, 'tesis_app/prediagnostico.html', {'form': form})

            # Crear un DataFrame para la predicción
            X_nuevo = pd.DataFrame([datos], columns=[
                'Fiebre',
                'Dolor_articulaciones',
                'Dolor_detras_de_ojos',
                'Dolor_muscular',
                'Dolor_de_cabeza',
                'Erupcion_cutanea_sarpullido',
                'Nauseas_vomitos',
                'Dolor_abdominal_intenso',
                'Vomitos_persistentes',
                'Sangrado_mucosas_y_encias',
                'Somnolencia_irritabilidad',
                'Decaimiento'
            ])

            # Realizar la predicción
            resultado = modelo.predict(X_nuevo)

            # Guardar el resultado de la predicción
            examen.resultado = resultado[0]  # Asignar el resultado al examen

            # Guardar el examen
            examen.save()

            messages.success(request, '¡Registro exitoso! El examen ha sido guardado correctamente.')
            form = ExamenForm()  # Reiniciar el formulario
            return render(request, 'tesis_app/prediagnostico.html', {'form': form})

    else:
        form = ExamenForm()

    return render(request, 'tesis_app/prediagnostico.html', {'form': form})

def historial(request):
    # Obtener todos los exámenes del usuario
    examenes = Examen.objects.filter(user=request.user)
    
    # Filtros de fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    tipo_dengue = request.GET.get('tipo_dengue')

    # Filtrar por fecha
    if fecha_inicio:
        examenes = examenes.filter(fsintomas__gte=fecha_inicio)
    if fecha_fin:
        examenes = examenes.filter(fsintomas__lte=fecha_fin)

    # Filtrar por tipo de dengue
    if tipo_dengue:
        examenes = examenes.filter(resultado=tipo_dengue)

    # Contar resultados
    positivos = examenes.filter(resultado='2').count()  # Contar positivos y dengue grave
    negativos = examenes.filter(resultado='1').count()  # Negativos
    dengue_grave = examenes.filter(resultado='3').count()  # Contar dengue grave (opcional)
    total_atendidos = examenes.count()

    return render(request, 'tesis_app/historial.html', {
        'examenes': examenes,
        'positivos': positivos,
        'negativos': negativos,
        'dengue_grave': dengue_grave,  # Si necesitas este conteo también
        'total_atendidos': total_atendidos,
    })
def perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'tesis_app/perfil.html', {'form': form})
from django.shortcuts import redirect

def home(request):
    return redirect('login')  # Redirige a la vista de inicio de sesión

def detalle_examen(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    return render(request, 'tesis_app/detalle_examen.html', {'examen': examen})

