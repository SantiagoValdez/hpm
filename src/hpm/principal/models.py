from django.db import models

# Create your models here.

class Usuario(models.Model):
    """
    Clase Usuario
    """
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
    """
    Clase Proyecto
    """
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
    """
    Clase Rol
    """
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
    """
    Clase Permiso
    """
    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'

    def __unicode__(self):
        return self.nombre

    nombre = models.CharField(max_length=50) 
    valor = models.IntegerField()

class Comite(models.Model):
    """
    Clase Comite
    """
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
    """
    Clase TipoItem
    """
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
    """
    Clase AtributoTipoItem
    """
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

class VersionItem(models.Model):
    class Meta:
        verbose_name = 'VersionItem'
        verbose_name_plural = 'VersionesItems'

    def __unicode__(self):
        return str(self.id)

    version = models.DateTimeField(auto_now=True, auto_now_add=True )
    complejidad = models.IntegerField()
    costo = models.IntegerField()
    prioridad = models.IntegerField()
    estado = models.TextField(max_length=50)

    proxy = models.ForeignKey('Item')
    atributos = models.ManyToManyField('AtributoItem',null=True, blank=True, default = None)

class Item(models.Model):
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
    def __unicode__(self):
        return self.nombre
    nombre = models.TextField(max_length=50)
    numero = models.IntegerField()
    eliminado = models.BooleanField(default = False)
    version = models.DateTimeField(null=True)
    id_actual = models.IntegerField(null=True)

    fase = models.ForeignKey(Fase)
    tipo_item = models.ForeignKey(TipoItem)
    linea_base = models.ForeignKey('LineaBase', null=True, blank=True, default = None, on_delete=models.CASCADE)
    
class Relacion(models.Model):
    class Meta:
        verbose_name = 'Relacion'
        verbose_name_plural = 'Relaciones'

    def __unicode__(self):
        pass
    tipo = models.TextField(max_length=50)

    #Guarda la referencia al item antecesor o padre
    antecesor = models.ForeignKey(VersionItem, related_name='relacion_antecesor_set')
    #Guarda la referencia al item sucesor o hijo
    sucesor = models.ForeignKey(VersionItem, related_name='relacion_sucesor_set')
    
    proyecto = models.ForeignKey(Proyecto)
    fase = models.ForeignKey(Fase)

class LineaBase(models.Model):
    """
    Clase LineaBase
    """
    class Meta:
        verbose_name = 'LineaBase'
        verbose_name_plural = 'LineasBase'

    def __unicode__(self):
        return self.nombre

    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, null=True)
    nombre = models.TextField(max_length=50)
    nro = models.IntegerField()
    # estados posibles: valido, no valido y liberado
    # estados posibles gab: inicial, en desarrollo,
    # con lineas de base parciales, linea base, finalizado
    estado = models.TextField()
