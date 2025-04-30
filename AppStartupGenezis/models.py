from django.db import models
from django.contrib.auth.models import User

# Institución
class Institucion(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=150)
    contacto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Paciente
class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=150)
    obra_social = models.BooleanField(default=False)
    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

# Médico
class Medico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    matricula = models.CharField(max_length=30)
    especialidad = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Dr/a. {self.nombre} - {self.especialidad}"

# Turno
class Turno(models.Model):
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=50)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha_hora} - {self.medico} - {self.paciente}"

# Historial Médico
class HistorialMedico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='historiales/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Historial de {self.paciente} - {self.fecha_subida.date()}"

    class Perfil(models.Model):
        ROLES = (
            ('paciente', 'Paciente'),
            ('medico', 'Médico'),
            ('admin', 'Administrador'),
        )
        usuario = models.OneToOneField(User, on_delete=models.CASCADE)
        rol = models.CharField(max_length=20, choices=ROLES)

        def __str__(self):
            return f"{self.usuario.username} - {self.rol}"