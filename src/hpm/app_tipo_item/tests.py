from django.test import TestCase
from django.utils import timezone
from principal.models import Proyecto, Fase, TipoItem, AtributoTipoItem

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

def crear_fase(nombre, descripcion, proyecto):
	"""
	Funcion: Encargada de crear una fase para realizacion de pruebas
	"""
	nrofases = Fase.objects.count() + 1
	f = Fase.objects.create(nro=nrofases, nombre=nombre, descripcion=descripcion, proyecto=proyecto)
		
	return f

def crear_tipo_item(nombre, codigo, descripcion, proyecto, fase):
	"""
	Funcion: Encargada de crear un tipo de item para realizacion de pruebas
	"""
	ti = TipoItem.objects.create(nombre=nombre, codigo=codigo, 
								descripcion=descripcion, proyecto=proyecto,
								fase=fase
								)
	return ti

def crear_atributo_tipo_item(nombre, tipo, valorpordefecto, tipoitem):
	"""
	Funcion: Encargada de crear un atributo de tipo de item para realizacion de pruebas
	"""
	tat = AtributoTipoItem.objects.create(nombre=nombre, tipo=tipo,
										 valor_por_defecto=valorpordefecto, 
										 tipo_item=tipoitem
										 )
	return tat

class TipoItemTest(TestCase):

	def test_creacion_tipoitem(self):
		"""
		Se comprueba que el tipo de item es creado exitosamente
		"""
		proyecto = crear_proyecto("Proyecto1", "Descripcion1", timezone.now(), 0, "no iniciado")
		proyecto.save()
		fase = crear_fase("Fase test", "descripcion test", proyecto)
		fase.save()
		tipoitem = crear_tipo_item("tipo item test", "testcod", "descripcion ti test", proyecto, fase)
		tipoitem_id = tipoitem.id
		tipoitem.save()

		ti = TipoItem.objects.get(id=tipoitem_id)
		self.assertEqual(ti.nombre,"tipo item test")

	def test_eliminacion_proyecto_tipoitem(self):
		"""
		Se comprueba que al eliminar el proyecto, todos los tipos de item
		asociados a las fases del mismo tambien son eliminados
		"""
		proyecto = crear_proyecto("Proyecto1", "Descripcion1", timezone.now(), 0, "no iniciado")
		proyecto.save()
		fase = crear_fase("Fase test", "descripcion test", proyecto)
		fase.save()
		tipoitem = crear_tipo_item("tipo item test", "testcod", "descripcion ti test", proyecto, fase)
		tipoitem_id = tipoitem.id
		tipoitem.save()

		proyecto.delete()
		nrotipoitem = TipoItem.objects.all()
		self.assertEqual(nrotipoitem.count(),0)

	def test_creacion_atributo(self):
		"""
		Se comprueba que el atributo de tipo de item es creado exitosamente
		"""
		proyecto = crear_proyecto("Proyecto1", "Descripcion1", timezone.now(), 0, "no iniciado")
		proyecto.save()
		fase = crear_fase("Fase test", "descripcion test", proyecto)
		fase.save()
		tipoitem = crear_tipo_item("tipo item test", "testcod", "descripcion ti test", proyecto, fase)
		#tipoitem_id = tipoitem.id
		tipoitem.save()

		atributo = crear_atributo_tipo_item("Atributo test", "integer", "0", tipoitem)
		atributo_id = atributo.id
		tatributo = AtributoTipoItem.objects.get(id=atributo_id)
		self.assertEqual(tatributo.id, atributo_id)
		tnombretipoitem = atributo.tipo_item.nombre
		self.assertEqual(tnombretipoitem, tipoitem.nombre)

	def test_eliminacion_atributo(self):
		"""
		Se comprueba que el atributo de tipo de item es eliminado exitosamente
		"""
		proyecto = crear_proyecto("Proyecto1", "Descripcion1", timezone.now(), 0, "no iniciado")
		proyecto.save()
		fase = crear_fase("Fase test", "descripcion test", proyecto)
		fase.save()
		tipoitem = crear_tipo_item("tipo item test", "testcod", "descripcion ti test", proyecto, fase)
		#tipoitem_id = tipoitem.id
		tipoitem.save()

		atributo = crear_atributo_tipo_item("Atributo test", "integer", "0", tipoitem)
		atributo_id = atributo.id
		tatributo = AtributoTipoItem.objects.get(id=atributo_id)
		self.assertEqual(tatributo.id, atributo_id)
		tnombretipoitem = atributo.tipo_item.nombre
		self.assertEqual(tnombretipoitem, tipoitem.nombre)

		tipoitem.delete()
		tipoitem.save()
		tatributo = AtributoTipoItem.objects.filter(tipo_item=tipoitem)
		self.assertEqual(tatributo.count(),0)