from django.test import TestCase

from principal.models import Rol

# Create your tests here.


def crear_rol(nombre, descripcion):
	"""
	Funcion: Encargada de crear un rol para realizacion de pruebas
	"""
	return Rol.objects.create(nombre=nombre, descripcion=descripcion)

class RolTest(TestCase):

	def test_creacion_rol(self):
		"""
		Se comprueba que el rol es creado exitosamente
		"""
		r = crear_rol("Administrador proyectoTest", "rol de prueba")
		r.save()
		tr = Rol.objects.get(nombre="Administrador proyectoTest")
		self.assertEqual(tr.nombre, "Administrador proyectoTest")

	def test_eliminacion_proyecto(self):
		"""
		Se comprueba que la eliminacion del rol se realiza con exito
		"""
		r = crear_rol("Administrador proyectoTest", "rol de prueba")
		r.save()

		r = Rol.objects.get(nombre="Administrador proyectoTest").delete()
		tr = Rol.objects.all()

		self.assertEqual(tr.count(), 0)