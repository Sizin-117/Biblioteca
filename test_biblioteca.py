import unittest
from Busqueda1 import NodoArbol, Biblioteca

class TestNodoArbol(unittest.TestCase):
    """Pruebas unitarias para la clase NodoArbol."""

    def setUp(self):
        self.raiz = NodoArbol("123", {"123": {"titulo": "Libro A", "autor": "Autor A", "anio": "2020"}})

    def test_insertar_nueva_clave(self):
        self.raiz.insertar("456", {"456": {"titulo": "Libro B", "autor": "Autor B", "anio": "2021"}})
        self.assertIsNotNone(self.raiz.derecha)
        self.assertEqual(self.raiz.derecha.clave, "456")

    def test_insertar_clave_existente(self):
        self.raiz.insertar("123", {"123": {"titulo": "Libro A2", "autor": "Autor A", "anio": "2022"}})
        self.assertEqual(len(self.raiz.datos), 2)

    def test_buscar_existente(self):
        resultado = self.raiz.buscar("123")
        self.assertIsInstance(resultado, list)
        self.assertEqual(resultado[0]["123"]["titulo"], "Libro A")

    def test_buscar_inexistente(self):
        resultado = self.raiz.buscar("999")
        self.assertIsNone(resultado)


class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        self.biblio = Biblioteca()
        self.biblio.libros = {
            "001": {"titulo": "A", "autor": "X", "anio": "1999"},
            "002": {"titulo": "B", "autor": "Y", "anio": "2000"},
            "003": {"titulo": "C", "autor": "Z", "anio": "2021"}
        }
        self.biblio.arboles = {
            criterio: self.biblio.construir_arbol(criterio)
            for criterio in ['titulo', 'autor', 'anio']
        }

    def test_equivalencia_busqueda_por_titulo(self):
        resultado = self.biblio.arboles['titulo'].buscar("A")
        self.assertIsNotNone(resultado)
        self.assertEqual(list(resultado[0].keys())[0], "001")

    def test_equivalencia_busqueda_por_autor_inexistente(self):
        resultado = self.biblio.arboles['autor'].buscar("Desconocido")
        self.assertIsNone(resultado)

    def test_valor_limite_anio_minimo(self):
        self.biblio.libros["004"] = {"titulo": "D", "autor": "W", "anio": "0000"}
        self.biblio.arboles['anio'] = self.biblio.construir_arbol('anio')
        resultado = self.biblio.arboles['anio'].buscar("0000")
        self.assertIsNotNone(resultado)

    def test_valor_limite_anio_maximo(self):
        self.biblio.libros["005"] = {"titulo": "E", "autor": "V", "anio": "9999"}
        self.biblio.arboles['anio'] = self.biblio.construir_arbol('anio')
        resultado = self.biblio.arboles['anio'].buscar("9999")
        self.assertIsNotNone(resultado)

    def test_valor_limite_titulo_vacio(self):
        self.biblio.libros["006"] = {"titulo": "", "autor": "U", "anio": "2022"}
        self.biblio.arboles['titulo'] = self.biblio.construir_arbol('titulo')
        resultado = self.biblio.arboles['titulo'].buscar("")
        self.assertIsNotNone(resultado)


if __name__ == '__main__':
    unittest.main()
