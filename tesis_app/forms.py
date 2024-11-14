from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Examen

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms


class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = [
            'fsintomas',
            'fiebre',
            'dolor_articulaciones',
            'dolor_detras_de_ojos',
            'dolor_muscular',
            'dolor_de_cabeza',
            'erupcion_cutanea',
            'nauseas_vomitos',
            'dolor_abdominal_intenso',
            'vomitos_persistentes',
            'sangrado_mucosas_y_encias',
            'somnolencia_irritabilidad',
            'decaimiento',
            'otros',
        ]
        widgets = {
            'fsintomas': forms.DateInput(attrs={'type': 'date'}),
            'otros': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe otros síntomas aquí...'}),
            # Usar CheckboxInput para los síntomas
            'fiebre': forms.CheckboxInput(),
            'dolor_articulaciones': forms.CheckboxInput(),
            'dolor_detras_de_ojos': forms.CheckboxInput(),
            'dolor_muscular': forms.CheckboxInput(),
            'dolor_de_cabeza': forms.CheckboxInput(),
            'erupcion_cutanea': forms.CheckboxInput(),
            'nauseas_vomitos': forms.CheckboxInput(),
            'dolor_abdominal_intenso': forms.CheckboxInput(),
            'vomitos_persistentes': forms.CheckboxInput(),
            'sangrado_mucosas_y_encias': forms.CheckboxInput(),
            'somnolencia_irritabilidad': forms.CheckboxInput(),
            'decaimiento': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ExamenForm, self).__init__(*args, **kwargs)
        # Establecer valores predeterminados para los checkboxes
        self.initial['fiebre'] = False
        self.initial['dolor_articulaciones'] = False
        self.initial['dolor_detras_de_ojos'] = False
        self.initial['dolor_muscular'] = False
        self.initial['dolor_de_cabeza'] = False
        self.initial['erupcion_cutanea'] = False
        self.initial['nauseas_vomitos'] = False
        self.initial['dolor_abdominal_intenso'] = False
        self.initial['vomitos_persistentes'] = False
        self.initial['sangrado_mucosas_y_encias'] = False
        self.initial['somnolencia_irritabilidad'] = False
        self.initial['decaimiento'] = False
        
class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']