from django.db import models
from django.contrib.auth.models import User

class Examen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fsintomas = models.DateField()
    fiebre = models.BooleanField()
    dolor_articulaciones = models.BooleanField()
    dolor_detras_de_ojos = models.BooleanField()
    dolor_muscular = models.BooleanField()
    dolor_de_cabeza = models.BooleanField()
    erupcion_cutanea = models.BooleanField()
    nauseas_vomitos = models.BooleanField()
    dolor_abdominal_intenso = models.BooleanField()
    vomitos_persistentes = models.BooleanField(null=True)
    sangrado_mucosas_y_encias = models.BooleanField(null=True)
    somnolencia_irritabilidad = models.BooleanField(null=True)
    decaimiento = models.BooleanField(null=True)
    otros = models.TextField(blank=True, null=True, max_length=300)
    resultado = models.CharField(blank=True, null=True, max_length=30)
    tiempo_deteccion = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Historial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)