import reflex as rx
from ..app_state import LibroState, AdminState 

# Decorador que define una nueva página en la aplicación para agregar un libro
@rx.page(route="/admin/agregar-libro", title="Agregar Libro")
def agregar_libro_admin():
    # Retorna una estructura condicional basada en la autenticación del usuario
    return rx.cond(
        AdminState.is_authenticated,  # Verifica si el usuario está autenticado
        rx.form(  # Crea un formulario para agregar un nuevo libro
            rx.vstack(  # Crea un contenedor vertical para los elementos del formulario
                rx.heading("Agregar un nuevo libro"),  # Encabezado del formulario
                rx.input("Título", on_change=LibroState.set_title),  # Campo de entrada para el título del libro
                rx.input("Autor", on_change=LibroState.set_author),  # Campo de entrada para el autor del libro
                rx.input("Precio", type="number", on_change=LibroState.set_price),  # Campo de entrada para el precio del libro
                rx.input("Stock", type="number", on_change=LibroState.set_stock),  # Campo de entrada para el stock disponible
                rx.upload(  # Componente para subir la imagen del libro
                    "Imagen del Libro",  
                    id="upload_book_image",  
                    border="1px dotted rgb(107,99,246)",  # Estilo del borde del área de carga
                    padding="5em",  # Espaciado interno del área de carga
                ),
                rx.button(  # Botón para agregar el libro
                    "Agregar",
                    on_click=lambda: handle_add_book(),  # Llama a la función handle_add_book al hacer clic
                ),
                rx.link("Volver al panel de administración", href="/admin"),  # Enlace para volver al panel de administración
            )
        ),
        rx.text("No tienes acceso a esta sección.")  # Mensaje para usuarios no autenticados
    )

# Función que maneja la lógica para agregar un nuevo libro
def handle_add_book():
    # Verifica que todos los campos requeridos estén completos y válidos
    if not (LibroState.title and LibroState.author and LibroState.price > 0 and LibroState.stock >= 0):
        return rx.alert("Por favor completa todos los campos correctamente.")
    
    # Intenta obtener los archivos subidos desde el componente de carga de imágenes
    image_files = rx.upload_files(upload_id="upload_book_image")
    if not image_files:  # Verifica que se haya subido una imagen válida
        return rx.alert("Por favor sube una imagen válida.")

    # Llama al método para agregar el libro al estado de la aplicación con los archivos de imagen
    LibroState.agregar_libro(image_files)
    return rx.alert("¡Libro agregado exitosamente!")  # Mensaje de éxito al agregar el libro