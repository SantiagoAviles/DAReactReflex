import reflex as rx
from ..app_state import AdminState, LibroState 

@rx.page(route="/admin", title="Panel de Administración")
def admin():
    return rx.cond(
        AdminState.is_authenticated, 
        rx.vstack(
            rx.heading("Panel de Administración"),
            rx.link("Cerrar sesión", on_click=AdminState.logout),
            rx.link("Volver al inicio", href="/"),
            rx.link("Agregar un nuevo libro", href="/admin/agregar-libro"), 
            rx.foreach(
                LibroState.libros, 
                lambda libro: rx.box(
                    rx.text(f"Título del libro: {libro.title}"), 
                    rx.text(f"Autor(es): {libro.author}"), 
                    rx.text(f"Precio: ${libro.price:.2f}"),
                    rx.text(f"Stock disponible: {libro.stock}"), 
                    rx.image(src=libro.image_path, alt="Imagen referencial", width="100px"), 
                    rx.button("Modificar", on_click=lambda: LibroState.mostrar_formulario_modificar(libro.id)),
                    rx.button("Eliminar", on_click=lambda: LibroState.eliminar_libro(libro.id)), 
                    border="1px solid gray", padding="4", margin="2"
                )
            ), spacing="4" 
        ),
        rx.text("No tienes acceso a esta sección.")
    )