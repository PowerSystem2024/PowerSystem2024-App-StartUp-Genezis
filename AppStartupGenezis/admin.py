from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Paciente, Medico, Institucion, Turno, HistorialMedico

admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Institucion)
admin.site.register(Turno)
admin.site.register(HistorialMedico)