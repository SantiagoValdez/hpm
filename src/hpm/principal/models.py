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

class Fase(models.Model):
    """
    Clase Fase
    """
    class Meta:
        verbose_name = 'Fase'
        verbose_name_plural = 'Fases'

    def __unicode__(self):
        return self.nombre

    nro = models.IntegerField()
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=250)
    #estados posible "inicial","en desarrollo", "con lineas de base parciales"
    # "con linea base", "finalizada"
    estado = models.CharField(max_length=30)
    #Cambiar para que no permita null
    proyecto = models.ForeignKey(Proyecto,null=True, blank=True, default = None, on_delete=models.CASCADE)

class TipoItem(models.Model):
    class Meta:
        verbose_name = 'TipoItem'
        verbose_name_plural = 'TipoItems'

    def __unicode__(self):
        return self.nombre
    
    nombre = models.TextField(max_length=50, unique=True)
    codigo = models.TextField(max_length=50, unique=True)
    descripcion = models.TextField(max_length=250)
    proyecto = models.ForeignKey(Proyecto)
    fase = models.ForeignKey(Fase)

class AtributoTipoItem(models.Model):
    class Meta:
        verbose_name = 'AtributoTipoItem'
        verbose_name_plural = 'AtributoTipoItems'

    def __unicode__(self):
        return self.nombre

    nombre = models.TextField(max_length=50)
    tipo = models.TextField(max_length=50)
    valor_por_defecto = models.TextField(max_length=50)

    tipo_item = models.ForeignKey(TipoItem)
    

class AtributoItem(models.Model):
    class Meta:
        verbose_name = 'AtributoItem'
        verbose_name_plural = 'AtributosItems'

    def __unicode__(self):
        return str(self.id)
    
    valor = models.TextField(max_length=150)
    atributo_tipo_item = models.ForeignKey(AtributoTipoItem)

class Item(models.Model):
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __unicode__(self):
        return str(self.id)

    version = models.IntegerField()
    complejidad = models.IntegerField()
    costo = models.IntegerField()
    prioridad = models.IntegerField()
    estado = models.TextField(max_length=50)


    

class ProxyItem(models.Model):
    class Meta:
        verbose_name = 'ProxyItem'
        verbose_name_plural = 'ProxyItems'

    def __unicode__(self):
        return self.nombre

    nombre = models.TextField(max_length=50)
    numero = models.IntegerField()
    eliminado = models.BooleanField(default = False)

    fase = models.ForeignKey(Fase)
    tipo_item = models.ForeignKey(TipoItem)

    