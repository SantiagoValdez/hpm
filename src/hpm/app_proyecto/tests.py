from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.utils import timezone
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from principal.models import Proyecto
from principal.models import Rol
from principal.models import Permiso

# Create your tests here.

def crear_proyecto(nombre, descripcion, fecha_creacion, complejidad_total, estado):
	"""
	Funcion: Encargada de crear un proyecto para realizacion de pruebas
	"""
	return Proyecto.objects.create(nombre=nombre, descripcion=descripcion,
								 fecha_creacion=fecha_creacion,
								 complejidad_total=complejidad_total,
								 estado=estado
								 )

def crear_rol(nombre, descripcion):
	"""
	Funcion: Encargada de crear un rol para realizacion de pruebas
	"""
	return Rol.objects.create(nombre=nombre, descripcion=descripcion)

def crear_permiso(nombre, valor):
	"""
	Funcion: Encargada de crear un permiso para la realizacion de pruebas
	"""
	return Permiso.objects.create(nombre=nombre, valor=valor)

class ProyectoTest(TestCase):

	def test_creacion_proyecto(self):
		"""
		Se comprueba que el proyecto es creado exitosamente
		"""
		p = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
		tp = Proyecto.objects.get(nombre="proyectoTest")
		self.assertEqual(tp.nombre, "proyectoTest")

	def test_eliminacion_proyecto(self):
		"""
		Se comprueba que al eliminar el proyecto, todos los roles
		asociado al mismo tambien son eliminados
		"""
		p = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
		r = crear_rol("Administrador proyectoTest", "rol de prueba")
		r.proyecto = p
		r.save()
		pr = crear_permiso("crear",0)
		r.permisos.add(pr)
		pr = crear_permiso("modificar",0)
		r.permisos.add(pr)

		Proyecto.objects.get(nombre="proyectoTest").delete()
		tp = Proyecto.objects.all()
		r = Rol.objects.all()
		self.assertEqual(len(tp), 0)
		self.assertEqual(len(r), 0)