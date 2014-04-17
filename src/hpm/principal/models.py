from django.db import models

class Usuario(models.Model):
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __unicode__(self):
        pass
    
    username = models.CharField(max_length=45, unique = True)
    password = models.CharField(max_length=45)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.CharField(max_length=20)
    ci = models.IntegerField()
    email = models.CharField(max_length=45)
        
class Proyecto(models.Model):
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __unicode__(self):
        pass
    
    
    nombre = models.CharField(unique = True, max_length=50)
    descripcion = models.CharField(max_length=250)
    