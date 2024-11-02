# Importamos la biblioteca reflex y los módulos necesarios
import reflex as rx
from .app_state import inicializar_datos  # Importamos la función para inicializar los datos de la aplicación
from .pages.index import index  # Importamos la página principal (índice)
from .pages.catalogo import catalogo  # Importamos la página del catálogo
from .pages.detalle_libro import detalle_libro  # Importamos la página de detalles del libro
from .pages.agregar_libro_admin import agregar_libro_admin  # Importamos la página para agregar libros como administrador
from .pages.login import login  # Importamos la página de inicio de sesión
from .pages.admin import admin  # Importamos la página de administración

# Creamos una instancia de la aplicación Reflex
app = rx.App()

# Agregamos las páginas a la aplicación con sus respectivas rutas
app.add_page(index)  # Página principal sin ruta específica
app.add_page(catalogo)  # Página del catálogo sin ruta específica
app.add_page(detalle_libro, route="/detalle-libro/[book_id]")  # Página de detalles del libro con un parámetro dinámico book_id
app.add_page(agregar_libro_admin, route="/admin/agregar-libro")  # Página para agregar libros, accesible solo para administradores
app.add_page(login, route="/login")  # Página de inicio de sesión
app.add_page(admin, route="/admin")  # Página de administración

# Si este archivo es ejecutado directamente, iniciamos el servidor de la aplicación
if __name__ == "__main__":
    app.run()  # Ejecuta la aplicación Reflex