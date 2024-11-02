import reflex as rx
from ..app_state import LibroState, AdminState 

@rx.page(route="/admin/agregar-libro", title="Agregar Libro")
def agregar_libro_admin():
    return rx.cond(
        AdminState.is_authenticated,
        rx.form(
            rx.vstack(
                rx.heading("Agregar un nuevo libro"), 
                rx.input("Título", on_change=LibroState.set_title), 
                rx.input("Autor", on_change=LibroState.set_author),
                rx.input("Precio", type="number", on_change=LibroState.set_price), 
                rx.input("Stock", type="number", on_change=LibroState.set_stock), 
                rx.upload(
                    "Imagen del Libro",  
                    id="upload_book_image",  
                    border="1px dotted rgb(107,99,246)",
                    padding="5em",
                ),
                rx.button(
                    "Agregar",
                    on_click=lambda: handle_add_book(), 
                ),
                rx.link("Volver al panel de administración", href="/admin"), 
            )
        ),
        rx.text("No tienes acceso a esta sección.")  
    )

def handle_add_book():
    if not (LibroState.title and LibroState.author and LibroState.price > 0 and LibroState.stock >= 0):
        return rx.alert("Por favor completa todos los campos correctamente.")
    
    image_files = rx.upload_files(upload_id="upload_book_image")
    if not image_files:
        return rx.alert("Por favor sube una imagen válida.")

    LibroState.agregar_libro(image_files)
    return rx.alert("¡Libro agregado exitosamente!") 