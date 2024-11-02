# Importamos la biblioteca reflex y los estados necesarios
import reflex as rx
from ..app_state import AdminState, LibroState  # Importamos los estados para la administración y libros

# Definimos la página de administración con su ruta y título
@rx.page(route="/admin", title="Panel de Administración")
def admin():
    # Usamos rx.cond para mostrar contenido basado en si el administrador está autenticado
    return rx.cond(
        AdminState.is_authenticated,  # Verificamos si el administrador está autenticado
        rx.vstack(  # Si está autenticado, mostramos el contenido del panel
            rx.heading("Panel de Administración"),  # Título del panel
            rx.link("Cerrar sesión", on_click=AdminState.logout),  # Enlace para cerrar sesión
            rx.link("Volver al inicio", href="/"),  # Enlace para volver a la página principal
            rx.link("Agregar un nuevo libro", href="/admin/agregar-libro"),  # Enlace para agregar un nuevo libro
            rx.foreach(  # Iteramos sobre la lista de libros en LibroState
                LibroState.libros, 
                lambda libro: rx.box(  # Para cada libro, creamos una caja con su información
                    rx.text(f"Título del libro: {libro.title}"),  # Muestra el título del libro
                    rx.text(f"Autor(es): {libro.author}"),  # Muestra el autor del libro
                    rx.text(f"Precio: ${libro.price:.2f}"),  # Muestra el precio del libro formateado a dos decimales
                    rx.text(f"Stock disponible: {libro.stock}"),  # Muestra el stock disponible del libro
                    rx.image(src=libro.image_path, alt="Imagen referencial", width="100px"),  # Muestra la imagen del libro
                    rx.button("Modificar", on_click=lambda: LibroState.mostrar_formulario_modificar(libro.id)),  # Botón para modificar el libro
                    rx.button("Eliminar", on_click=lambda: LibroState.eliminar_libro(libro.id)),  # Botón para eliminar el libro
                    border="1px solid gray", padding="4", margin="2"  # Estilos de la caja que contiene los detalles del libro
                )
            ), spacing="4"  # Espaciado entre los elementos de la lista de libros
        ),
        rx.text("No tienes acceso a esta sección.")  # Mensaje mostrado si no está autenticado
    )