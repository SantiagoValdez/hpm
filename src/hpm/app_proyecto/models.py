from django.db import models

# Create your models here.

class Proyecto(models.Model):
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __unicode__(self):
        return self.nombre
    
    
    nombre = models.CharField(unique = True, max_length=50)
    descripcion = models.CharField(max_length=250)
    fecha_creacion = models.DateField()
    complejidad_total = models.IntegerField(default=0)
    estado = models.CharField(max_length=45)