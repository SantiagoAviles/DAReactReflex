import reflex as rx
from sqlmodel import Field, select
from typing import List, Optional
from PIL import Image
import os

IMAGE_FOLDER = "img_libro"

class Libro(rx.Model, table=True):
    id: int = Field(default=None, primary_key=True) 
    title: str 
    author: str 
    price: float 
    stock: int 
    image_path: str 

class Admin(rx.Model, table=True):
    username: str = Field(primary_key=True)
    password: str  

class AdminState(rx.State):
    is_authenticated: bool = False 
    username: str = ""
    password: str = "" 

    def login(self):
        with rx.session() as session:
            admin = session.get(Admin, self.username) 
            if admin and admin.password == self.password: 
                self.is_authenticated = True 
            else:
                self.is_authenticated = False 

    def logout(self):
        self.is_authenticated = False

class LibroState(rx.State):
    libros: List[Libro] = []  
    title: str = "" 
    author: str = ""  
    price: float = 0.0  
    stock: int = 0  
    image_file: Optional[str] = None  
    quantity: int = 0 
    libro_a_modificar: Optional[Libro] = None 

    def set_title(self, title: str):
        self.title = title

    def set_author(self, author: str):
        self.author = author

    def set_price(self, price: float):
        self.price = price

    def set_stock(self, stock: str):
        try:
            stock_int = int(stock) 
            if stock_int < 0:
                raise ValueError("El stock no puede ser negativo.")
            self.stock = stock_int
        except ValueError:
            raise ValueError("El stock debe ser un número entero.") 

    def set_image_file(self, image_file: str):
        self.image_file = image_file

    def set_quantity(self, quantity: int):
        self.quantity = quantity  

    def cargar_libros(self):
        with rx.session() as session:
            self.libros = session.exec(Libro.select()).all()
    
    async def agregar_libro(self, uploaded_files: list[rx.UploadFile]):
        if uploaded_files:
            image_file = uploaded_files[0] 
            image_path = os.path.join(IMAGE_FOLDER, f"{self.title.replace(' ', '_')}.png") 
        
            upload_data = await image_file.read()

            with open(image_path, 'wb') as img_file:
                img_file.write(upload_data)

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

    def mostrar_formulario_modificar(self, libro_id: int):
        with rx.session() as session:
            libro = session.get(Libro, libro_id)
            if libro:
                self.libro_a_modificar = libro 
                self.title = libro.title
                self.author = libro.author
                self.price = libro.price
                self.stock = libro.stock
                self.image_file = libro.image_path

    def modificar_libro(self):
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

    def comprar_libro(self, libro_id: int):
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

    def eliminar_libro(self, libro_id: int):
        with rx.session() as session:
            libro = session.get(Libro, libro_id) 
            if libro:
                if os.path.exists(libro.image_path):
                    os.remove(libro.image_path) 
                session.delete(libro) 
                session.commit()  
                self.cargar_libros() 

    @staticmethod
    def obtener_detalles_libro(book_id: int) -> dict:
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

def inicializar_datos():
    with rx.session() as session:
        if not session.exec(select(Admin)).all():
            admin1 = Admin(username="admin1", password="adminpass1")
            admin2 = Admin(username="admin2", password="adminpass2")
            session.add(admin1)
            session.add(admin2)

        session.commit()