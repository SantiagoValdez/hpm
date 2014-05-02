# from django.test import TestCase

# # Create your tests here.

# from django.test import TestCase
# from django.utils import timezone
# from django.http import HttpResponse
# from django.core.urlresolvers import reverse

# from principal.models import Proyecto
# from principal.models import Rol
# from principal.models import Permiso

# # Create your tests here.

# def crear_proyecto(nombre, descripcion, fecha_creacion, complejidad_total, estado):
# 	return Proyecto.objects.create(nombre=nombre, descripcion=descripcion,
# 								 fecha_creacion=fecha_creacion,
# 								 complejidad_total=complejidad_total,
# 								 estado=estado
# 								 )

# def crear_rol(nombre, descripcion):
# 	return Rol.objects.create(nombre=nombre, descripcion=descripcion)

# def crear_permiso(nombre, valor):
# 	return Permiso.objects.create(nombre=nombre, valor=valor)

# class ProyectoTest(TestCase):

# 	def test_creacion_proyecto(self):
# 		p = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
# 		tp = Proyecto.objects.get(nombre="proyectoTest")
# 		self.assertEqual(tp.nombre, "proyectoTest")

# 	def test_eliminacion_proyecto(self):
# 		p = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
# 		r = crear_rol("Administrador proyectoTest", "rol de prueba")
# 		r.proyecto = p
# 		r.save()
# 		pr = crear_permiso("crear",0)
# 		r.permisos.add(pr)
# 		pr = crear_permiso("modificar",0)
# 		r.permisos.add(pr)

# 		Proyecto.objects.get(nombre="proyectoTest").delete()
# 		tp = Proyecto.objects.all()
# 		r = Rol.objects.all()
# 		self.assertEqual(len(tp), 0)
# 		self.assertEqual(len(r), 0)