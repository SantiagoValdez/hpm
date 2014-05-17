from django.test import TestCase
from django.utils import timezone
from principal.models import Proyecto, Comite

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

def crear_comite(proyecto):
	"""
	Funcion: Encargada de crear un comite para realizacion de pruebas
	"""
	return Comite.objects.create(proyecto=proyecto)

class ComiteTest(TestCase):

	def test_creacion_comite(self):
		"""
		Se comprueba que el comite es creado exitosamente
		"""
		tproyecto = crear_proyecto("Proyecto1", "Descripcion1", timezone.now(), 0, "no iniciado")
		tproyecto.save()
		tproyecto_id = tproyecto.id
		tcomite = crear_comite(tproyecto)
		tcomite.save()
		tcomiteproyecto_id = tcomite.proyecto.id
		self.assertEqual(tcomiteproyecto_id, tproyecto_id)

	def test_eliminacion_comite(self):
		"""
		Se comprueba que al eliminar el proyecto, el comite
		asociado al mismo tambien es eliminado
		"""
		tproyecto = crear_proyecto("Proyecto1", "Descripcion1", timezone.now(), 0, "no iniciado")
		tproyecto.save()
		tcomite = crear_comite(tproyecto)
		tcomite.save()
		tcomite_id = tcomite.id

		tproyecto.delete()
		tproyecto.save()
		tcomite = Comite.objects.all()
		self.assertEqual(tcomite.count(), 0)