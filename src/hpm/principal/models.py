from django.db import models

# Create your models here.

class Usuario(models.Model):
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __unicode__(self):
        return self.username
    
    username = models.CharField(max_length=45, unique = True)
    password = models.CharField(max_length=45)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.CharField(max_length=20)
    ci = models.IntegerField()
    email = models.CharField(max_length=45)
    roles = models.ManyToManyField('Rol',null=True, blank=True, default = None)

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
    
class Rol(models.Model):
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __unicode__(self):
        return self.nombre
    
    nombre = models.CharField(unique = True, max_length=45)
    descripcion = models.CharField(max_length=150)
    permisos = models.ManyToManyField('Permiso',null=True, blank=True, default = None)
    proyecto = models.ForeignKey(Proyecto,null=True, blank=True, default = None)


class Permiso(models.Model):

    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'

    def __unicode__(self):
        return self.nombre

    nombre = models.CharField(max_length=50) 
    valor = models.IntegerField()

class Comite(models.Model):
    class Meta:
        verbose_name = 'Comite'
        verbose_name_plural = 'Comites'

    def __unicode__(self):
        return "Comite " + str(self.proyecto)

    proyecto = models.ForeignKey(Proyecto, unique = True)
    usuarios = models.ManyToManyField('Usuario',null=True, blank=True, default = None)
