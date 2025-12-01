import time

class NodoArbol:
    def __init__(self, clave, datos):
        self.clave = clave
        self.datos = [datos]
        self.izquierda = None
        self.derecha = None

    def insertar(self, clave, datos):
        if clave == self.clave:
            self.datos.append(datos)
        elif clave < self.clave:
            if self.izquierda:
                self.izquierda.insertar(clave, datos)
            else:
                self.izquierda = NodoArbol(clave, datos)
        else:
            if self.derecha:
                self.derecha.insertar(clave, datos)
            else:
                self.derecha = NodoArbol(clave, datos)

    def buscar(self, clave):
        if clave == self.clave:
            return self.datos
        elif clave < self.clave and self.izquierda:
            return self.izquierda.buscar(clave)
        elif clave > self.clave and self.derecha:
            return self.derecha.buscar(clave)
        return None


class Biblioteca:
    # Simula una biblioteca con árboles binarios de búsqueda por criterios distintos. 

    def __init__(self):
        self.libros = {}
        self.arboles = {}

    def construir_arbol(self, criterio):
        # Construye un árbol binario a partir de los libros usando el criterio dado.
        claves = list(self.libros.keys())
        if not claves:
            return None

        primera_clave = claves[0]
        raiz = NodoArbol(self.libros[primera_clave][criterio], {primera_clave: self.libros[primera_clave]})

        for clave in claves[1:]:
            valor = self.libros[clave][criterio]
            raiz.insertar(valor, {clave: self.libros[clave]})
        return raiz


# --- Funciones de prueba de rendimiento ---

def medir_insercion(arbol, valores):
    inicio = time.time()
    for valor in valores:
        arbol.insertar(valor, f"Dato {valor}")
    return time.time() - inicio


def medir_busqueda(arbol, valores):
    inicio = time.time()
    for valor in valores:
        arbol.buscar(valor)
    return time.time() - inicio


if __name__ == "__main__":
    import random
    valores = random.sample(range(1, 1000), 100)
    raiz = NodoArbol(valores[0], f"Dato {valores[0]}")
    tiempo_insercion = medir_insercion(raiz, valores[1:])
    tiempo_busqueda = medir_busqueda(raiz, valores)
    print(f"Tiempo de inserción: {tiempo_insercion:.6f} s")
    print(f"Tiempo de búsqueda: {tiempo_busqueda:.6f} s")
