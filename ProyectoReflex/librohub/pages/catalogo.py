import reflex as rx
from ..app_state import LibroState

# Decorador que define una nueva página en la aplicación para el catálogo de libros
@rx.page(route="/catalogo", title="Catálogo de Libros")
def catalogo():
    try:
        # Intenta cargar la lista de libros desde el estado
        LibroState.cargar_libros()
    except Exception as e:
        # Si ocurre un error al cargar los libros, muestra un mensaje de error
        return rx.text(f"Error al cargar los libros: {str(e)}")

    # Verifica si no hay libros disponibles en el catálogo
    if not LibroState.libros:
        return rx.vstack(
            rx.heading("Catálogo de Libros"),  # Encabezado del catálogo
            rx.text("No hay libros disponibles en el catálogo."),  # Mensaje informativo
            rx.link("Agregar un nuevo libro", href="/login"),  # Enlace para agregar un nuevo libro (redirige a login)
            spacing="4",  # Espaciado entre los elementos
        )

    # Crea una lista de libros utilizando foreach para iterar sobre los libros cargados
    lista_libros = rx.foreach(
        LibroState.libros,
        lambda book: rx.box(  # Para cada libro, crea un contenedor con sus detalles
            rx.image(src=book.image_path, width="100px", height="150px"),  # Imagen del libro
            rx.text(f"Título: {book.title}"),  # Muestra el título del libro
            rx.text(f"Autor: {book.author}"),  # Muestra el autor del libro
            rx.text(f"Precio: ${book.price:.2f}"),  # Muestra el precio del libro formateado a dos decimales
            rx.text(f"Stock: {book.stock}"),  # Muestra la cantidad de stock disponible
            rx.link("Ver detalles", href=f"/detalle-libro/{book.id}"),  # Enlace para ver detalles del libro
            border="1px solid gray",  # Estilo del borde del contenedor del libro
            padding="4",  # Espaciado interno del contenedor
            margin="2",  # Margen externo del contenedor
            width="200px"  # Ancho del contenedor del libro
        )
    )

    # Retorna el contenido del catálogo con el encabezado y la lista de libros
    return rx.vstack(
        rx.heading("Catálogo de Libros"),  # Encabezado principal del catálogo
        lista_libros,  # Lista de libros generada anteriormente
        spacing="4",  # Espaciado entre los elementos del catálogo
    )