import reflex as rx
from sqlmodel import Field, SQLModel, select
from typing import List, Optional
from PIL import Image
import os

# Carpeta donde se almacenarán las imágenes de los libros
IMAGE_FOLDER = "img_libro"

# Modelo de datos para los libros
class Libro(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # ID del libro (clave primaria)
    title: str  # Título del libro
    author: str  # Autor del libro
    price: float  # Precio del libro
    stock: int  # Stock disponible del libro
    image_path: str  # Ruta de la imagen del libro

# Modelo de datos para los administradores
class Admin(SQLModel, table=True):
    username: str = Field(primary_key=True)  # Nombre de usuario (clave primaria)
    password: str  # Contraseña del administrador

# Clase que gestiona el estado de autenticación del administrador
class AdminState(rx.State):
    is_authenticated: bool = False  # Indica si el administrador está autenticado
    username: str = ""  # Nombre de usuario ingresado
    password: str = ""  # Contraseña ingresada

    def login(self):
        with rx.session() as session:
            admin = session.get(Admin, self.username)  # Busca al administrador por nombre de usuario
            if admin and admin.password == self.password:  # Verifica la contraseña
                self.is_authenticated = True  # Establece el estado como autenticado
            else:
                self.is_authenticated = False  # Establece el estado como no autenticado

    def logout(self):
        self.is_authenticated = False  # Cierra la sesión del administrador

# Clase que gestiona el estado de los libros en la aplicación
class LibroState(rx.State):
    libros: List[Libro] = []  # Lista de libros disponibles
    title: str = ""  # Título del libro a agregar/modificar
    author: str = ""  # Autor del libro a agregar/modificar
    price: float = 0.0  # Precio del libro a agregar/modificar
    stock: int = 0  # Stock del libro a agregar/modificar
    image_file: Optional[str] = None  # Archivo de imagen subido para el libro
    quantity: int = 0  # Cantidad a comprar del libro
    libro_a_modificar: Optional[Libro] = None  # Libro que se está modificando

    def set_title(self, title: str):
        self.title = title  # Establece el título del libro

    def set_author(self, author: str):
        self.author = author  # Establece el autor del libro

    def set_price(self, price: float):
        self.price = price  # Establece el precio del libro

    def set_stock(self, stock: str):
        try:
            stock_int = int(stock) 
            if stock_int < 0:
                raise ValueError("El stock no puede ser negativo.")  # Verifica que el stock no sea negativo
            self.stock = stock_int  # Establece el stock del libro
        except ValueError:
            raise ValueError("El stock debe ser un número entero.")  # Maneja errores en la conversión a entero

    def set_image_file(self, image_file: str):
        self.image_file = image_file  # Establece el archivo de imagen subido

    def set_quantity(self, quantity: int):
        self.quantity = quantity  # Establece la cantidad a comprar

    def cargar_libros(self):
        with rx.session() as session:
            self.libros = session.exec(Libro.select()).all()  # Carga todos los libros desde la base de datos
    
    async def agregar_libro(self, uploaded_files: list[rx.UploadFile]): # Función para agregar algún libro
        if uploaded_files:
            image_file = uploaded_files[0] 
            image_path = os.path.join(IMAGE_FOLDER, f"{self.title.replace(' ', '_')}.png") 
        
            upload_data = await image_file.read()  # Lee los datos del archivo subido

            with open(image_path, 'wb') as img_file:
                img_file.write(upload_data)  # Guarda la imagen en el sistema de archivos

        try:
            stock = int(self.stock)  
        except ValueError:
            raise ValueError("El stock debe ser un número entero.")  

        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")  

        with rx.session() as session:
            nuevo_libro = Libro(
                title=self.title, 
                author=self.author, 
                price=self.price, 
                stock=stock,
                image_path=image_path
            )
            session.add(nuevo_libro) 
            session.commit()  
            self.cargar_libros() 

    def mostrar_formulario_modificar(self, libro_id: int): # Función para mostrar el formulario para modificar datos de un libro
        with rx.session() as session:
            libro = session.get(Libro, libro_id)  
            if libro:
                self.libro_a_modificar = libro 
                self.title = libro.title
                self.author = libro.author
                self.price = libro.price
                self.stock = libro.stock
                self.image_file = libro.image_path

    def modificar_libro(self): # Función para modificar algún libro
        if self.libro_a_modificar:
            with rx.session() as session:
                libro = session.get(Libro, self.libro_a_modificar.id) 
                if libro:
                    libro.title = self.title 
                    libro.author = self.author
                    libro.price = self.price
                    if self.stock < 0:
                        raise ValueError("El stock no puede ser negativo.")
                    libro.stock = self.stock
                    
                    if self.image_file:
                        image_path = os.path.join(IMAGE_FOLDER, f"{self.title.replace(' ', '_')}.png")
                        image = Image.open(self.image_file)
                        image.save(image_path)  
                        libro.image_path = image_path
                    
                    session.add(libro) 
                    session.commit() 
                    self.cargar_libros() 
                    self.libro_a_modificar = None 

    def comprar_libro(self, libro_id: int): # Función para agregar un libro al carrito
        with rx.session() as session:
            libro = session.get(Libro, libro_id)  
            if libro:
                if self.quantity > 0 and self.quantity <= libro.stock:
                    libro.stock -= self.quantity  
                    session.add(libro) 
                    session.commit()  
                    self.cargar_libros()  
                else:
                    raise ValueError("Cantidad no válida para la compra.") 

    def eliminar_libro(self, libro_id: int): # Función para eliminar algún libro
        with rx.session() as session:
            libro = session.get(Libro, libro_id)  
            if libro:
                if os.path.exists(libro.image_path):  
                    os.remove(libro.image_path)  
                session.delete(libro) 
                session.commit()  
                self.cargar_libros() 

    @staticmethod
    def obtener_detalles_libro(book_id: int) -> dict: # Función para obtener detalles sobre el libro
        with rx.session() as session:
            libro = session.get(Libro, book_id)  
            if libro:
                return {
                    "title_text": f"Detalles del Libro: {libro.title}",
                    "author_text": f"Autor: {libro.author}",
                    "price_text": f"Precio: ${libro.price:.2f}", 
                    "stock": libro.stock,
                    "image_path": libro.image_path,
                }
            else:
                return {
                    "title_text": "Libro no encontrado",
                    "author_text": "",
                    "price_text": "",
                    "stock": 0,
                    "image_path": "",
                }

# Función para inicializar datos predeterminados en la base de datos (administradores)
def inicializar_datos():
    with rx.session() as session:
        if not session.exec(select(Admin)).all():  
            admin1 = Admin(username="admin1", password="adminpass1")  
            admin2 = Admin(username="admin2", password="adminpass2")  
            session.add(admin1)
            session.add(admin2)

        session.commit()