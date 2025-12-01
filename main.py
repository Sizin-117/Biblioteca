from collections import deque   # Para manejar colas de espera de libros
import json   # Para cargar datos iniciales desde un JSON


# -------------------- CLASE USUARIO --------------------
class User:
    def __init__(self, user_id, name, document):
        # Inicializa los atributos del usuario
        self.id = user_id
        self.name = name
        self.document = document

    def __str__(self):
        # Muestra los datos del usuario como texto
        return f"ID: {self.id} | Nombre: {self.name} | Documento: {self.document}"


# -------------------- CLASE LIBRO --------------------
class Book:
    def __init__(self, book_id, tittle, author, year):
        # Inicializa los atributos del libro
        self.id = book_id
        self.tittle = tittle
        self.author = author
        self.year = year
        self.available = True  # Indica si el libro está disponible
        self.queue_waiting = deque()  # Cola de usuarios que esperan el libro

    def __str__(self):
        # Muestra los datos del libro como texto
        status = "Disponible" if self.available else "Prestado"
        return f"ID: {self.id} | Título: {self.tittle} | Autor: {self.author} | Año: {self.year} | Estado: {status}"


# -------------------- CLASE NODO DEL ÁRBOL --------------------
class Node:
    def __init__(self, key, value):
        # Cada nodo del árbol almacena una clave, un valor y referencias a hijos
        self.key = key
        self.value = value
        self.left = None
        self.right = None


# -------------------- CLASE ÁRBOL BINARIO --------------------
class BinarySearchTree:
    def __init__(self):
        # El árbol empieza vacío
        self.root = None

    def insert(self, key, value):
        # Inserta un nuevo elemento en el árbol binario
        if not self.root:
            # Si no hay raíz, este será el primer nodo
            self.root = Node(key, value)
        else:
            # Si ya existe raíz, busca la posición correcta recursivamente
            self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        # Inserción recursiva según orden alfabético o numérico de la clave
        if key < node.key:
            if node.left:
                self._insert(node.left, key, value)
            else:
                node.left = Node(key, value)
        elif key > node.key:
            if node.right:
                self._insert(node.right, key, value)
            else:
                node.right = Node(key, value)
        else:
            # Si la clave ya existe, actualiza su valor
            node.value = value

    def search(self, key):
        # Busca un elemento por su clave
        return self._search(self.root, key)

    def _search(self, node, key):
        # Búsqueda recursiva: si la clave coincide, devuelve el valor
        if node is None:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def inorder(self):
        # Devuelve una lista con los valores en orden ascendente
        elements = []
        self._inorder(self.root, elements)
        return elements

    def _inorder(self, node, elements):
        # Recorrido inorden (izquierda - raíz - derecha)
        if node:
            self._inorder(node.left, elements)
            elements.append(node.value)
            self._inorder(node.right, elements)


# -------------------- CLASE BIBLIOTECA --------------------
class Library:
    def __init__(self):
        # Listas básicas para almacenar usuarios y libros
        self.users = []
        self.books = []

        # Árboles binarios para búsquedas más rápidas
        self.user_tree = BinarySearchTree()  # Buscar usuarios por documento
        self.book_tree = BinarySearchTree()  # Buscar libros por título

        # Carga inicial desde un JSON interno
        self.load_users_and_books_from_json()

    def load_users_and_books_from_json(self):
        # Carga los datos iniciales (usuarios y libros) desde archivos JSON separados.
        try:
            # Cargar usuarios
            with open("users.json", "r", encoding="utf-8") as file_users:
                users_data = json.load(file_users)
                for u in users_data:
                    user = User(u["id"], u["name"], u["document"])
                    self.users.append(user)
                    self.user_tree.insert(u["document"], user)

            # Cargar libros
            with open("books.json", "r", encoding="utf-8") as file_books:
                books_data = json.load(file_books)
                for b in books_data:
                    book = Book(b["id"], b["tittle"], b["author"], b["year"])
                    self.books.append(book)
                    self.book_tree.insert(b["tittle"].lower(), book)

        except FileNotFoundError as e:
            print(f"Archivo no encontrado: {e.filename}. Se iniciará con datos vacíos.")
        except json.JSONDecodeError as e:
            print(f"Error al leer JSON: {e}")

    # -------------------- USUARIOS --------------------
    def create_user(self):
        # Pide los datos del nuevo usuario
        name = input("Ingrese el nombre del usuario: ").strip()
        document = input("Ingrese el documento del usuario: ").strip()
        user_id = len(self.users) + 1

        # Crea el usuario y lo agrega tanto a la lista como al árbol
        new_user = User(user_id, name, document)
        self.users.append(new_user)
        self.user_tree.insert(document, new_user)
        print(f"✅ Usuario '{name}' creado con éxito.")

    def view_user(self):
        # Muestra los usuarios ordenados por documento (gracias al árbol)
        if not self.users:
            print("⚠️ No hay usuarios registrados.")
        else:
            for user in self.user_tree.inorder():
                print(user)

    def search_user_by_document(self, document=None):
        # Busca un usuario por su documento (usa el árbol)
        if document is None:
            document = input("Ingrese el documento del usuario a buscar: ").strip()
        return self.user_tree.search(document)

    # -------------------- LIBROS --------------------
    def add_book(self):
        # Pide los datos del nuevo libro
        tittle = input("Ingrese el título del libro: ").strip()
        author = input("Ingrese el autor del libro: ").strip()
        try:
            year = int(input("Ingrese el año del libro: "))
        except ValueError:
            print("⚠️ Año inválido.")
            return

        # Crea el libro y lo agrega tanto a la lista como al árbol
        book_id = len(self.books) + 1
        new_book = Book(book_id, tittle, author, year)
        self.books.append(new_book)
        self.book_tree.insert(tittle.lower(), new_book)
        print(f"✅ Libro '{tittle}' agregado con éxito.")

    def show_books(self):
        # Muestra los libros ordenados por título (gracias al árbol)
        if not self.books:
            print("⚠️ No hay libros registrados.")
        else:
            for book in self.book_tree.inorder():
                print(book)

    def search_book_by_tittle(self, tittle=None):
        # Busca un libro por su título (usa el árbol)
        if tittle is None:
            tittle = input("Ingrese el título del libro a buscar: ").strip()
        return self.book_tree.search(tittle.lower())

    # -------------------- PRÉSTAMOS --------------------
    def lend_book(self):
        # Pide documento y busca el usuario
        document = input("Documento del usuario: ").strip()
        user = self.search_user_by_document(document)
        if not user:
            print("❌ Usuario no encontrado.")
            return

        # Pide título y busca el libro
        tittle = input("Título del libro a prestar: ").strip()
        book = self.search_book_by_tittle(tittle)
        if not book:
            print("❌ Libro no encontrado.")
            return

        # Si el libro está disponible, se presta al usuario
        if book.available:
            book.available = False
            print(f"✅ El libro '{book.tittle}' ha sido prestado a {user.name}.")
        else:
            # Si no, se agrega a la cola de espera
            book.queue_waiting.append(user)
            print(f"📚 El libro '{book.tittle}' está prestado. {user.name} ha sido agregado a la cola de espera.")

    # -------------------- DEVOLUCIONES --------------------
    def return_book(self):
        # Pide el título del libro y lo busca
        tittle = input("Ingrese el título del libro a devolver: ").strip()
        book = self.search_book_by_tittle(tittle)
        if not book:
            print("❌ Libro no encontrado.")
            return

        # Si el libro ya estaba disponible, avisa
        if book.available:
            print(f"⚠️ El libro '{book.tittle}' ya estaba disponible.")
            return

        # Si hay personas en cola, se asigna al siguiente
        if book.queue_waiting:
            next_user = book.queue_waiting.popleft()
            print(f"🔁 El libro '{book.tittle}' ha sido asignado a {next_user.name} de la cola de espera.")
        else:
            # Si no hay cola, el libro vuelve a estar disponible
            book.available = True
            print(f"🔄 El libro '{book.tittle}' ha sido devuelto y ahora está disponible.")

    # -------------------- MENÚ PRINCIPAL --------------------
    def menu(self):
        # Menú interactivo de la biblioteca
        while True:
            print("\n📚 Menú de Biblioteca")
            print("1. Crear usuario")
            print("2. Ver usuarios (ordenados por documento)")
            print("3. Buscar usuario por documento")
            print("4. Agregar libro")
            print("5. Ver libros (ordenados por título)")
            print("6. Buscar libro por título")
            print("7. Prestar libro")
            print("8. Devolver libro")
            print("9. Salir")

            opcion = input("Seleccione una opción: ")

            # Se usa 'match' para manejar las opciones del menú
            match opcion:
                case "1":
                    self.create_user()
                case "2":
                    self.view_user()
                case "3":
                    user = self.search_user_by_document()
                    print(user if user else "Usuario no encontrado.")
                case "4":
                    self.add_book()
                case "5":
                    self.show_books()
                case "6":
                    book = self.search_book_by_tittle()
                    print(book if book else "Libro no encontrado.")
                case "7":
                    self.lend_book()
                case "8":
                    self.return_book()
                case "9":
                    print("👋 ¡Hasta pronto!")
                    break
                case _:
                    print("❌ Opción inválida. Intente de nuevo.")


# -------------------- EJECUCIÓN DEL PROGRAMA --------------------
# Se crea una instancia de la biblioteca y se inicia el menú
app = Library()
app.menu()
