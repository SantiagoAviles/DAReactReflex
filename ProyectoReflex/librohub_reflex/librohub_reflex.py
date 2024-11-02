import reflex as rx
from .app_state import inicializar_datos
from .pages.index import index 
from .pages.catalogo import catalogo 
from .pages.detalle_libro import detalle_libro 
from .pages.agregar_libro_admin import agregar_libro_admin 
from .pages.login import login 
from .pages.admin import admin 

app = rx.App()

app.add_page(index) 
app.add_page(catalogo) 
app.add_page(detalle_libro, route="/detalle-libro/[book_id]") 
app.add_page(agregar_libro_admin, route="/admin/agregar-libro") 
app.add_page(login, route="/login") 
app.add_page(admin, route="/admin") 

try:
    inicializar_datos()
except Exception as e:
    print(f"Error al inicializar datos: {e}")

if __name__ == "__main__":
    app.run()