from django.test import TestCase
from principal.models import Usuario

# Create your tests here.


class UsuarioTestCase(TestCase):
    def setUp(self):
        Usuario.objects.create(username="usera", nombre="A", apellido = "apellido", telefono = "telefono", password = "password", email = "email", ci = 0)
        Usuario.objects.create(username="userb", nombre="B", apellido = "apellido", telefono = "telefono", password = "password", email = "email", ci = 0)

    def test_nombre_correcto(self):
        """Test si se guardan correctamente los objetos"""
        a = Usuario.objects.get(username="usera")
        b = Usuario.objects.get(username="userb")
        self.assertEqual(a.nombre, 'A')
        self.assertEqual(b.nombre, 'B')