from django.db import models
# Create your models here.

class Bebida(models.Model):
	nombre = models.CharField(max_length=50)
	ingredientes = models.TextField()
	preparacion = models.TextField()
	def __unicode__(self):
		return self.nombre

class Usuario(models.Model):
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __unicode__(self):
        pass
    
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.CharField(max_length=20)
    ci = models.IntegerField()
    email = models.CharField(max_length=45)
        

