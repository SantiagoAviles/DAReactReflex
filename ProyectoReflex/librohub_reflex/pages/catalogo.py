import reflex as rx
from ..app_state import LibroState

@rx.page(route="/catalogo", title="Catálogo de Libros")
def catalogo():
    try:
        LibroState.cargar_libros()
    except Exception as e:
        return rx.text(f"Error al cargar los libros: {str(e)}")

    if not LibroState.libros:
        return rx.vstack(
            rx.heading("Catálogo de Libros"), 
            rx.text("No hay libros disponibles en el catálogo."),
            rx.link("Agregar un nuevo libro", href="/login"),
            spacing="4",
        )

    lista_libros = rx.foreach(
        LibroState.libros,
        lambda book: rx.box(
            rx.image(src=book.image_path, width="100px", height="150px"),
            rx.text(f"Título: {book.title}"),
            rx.text(f"Autor: {book.author}"),
            rx.text(f"Precio: ${book.price:.2f}"),
            rx.text(f"Stock: {book.stock}"), 
            rx.link("Ver detalles", href=f"/detalle-libro/{book.id}"), 
            border="1px solid gray", 
            padding="4", 
            margin="2",
            width="200px" 
        )
    )

    return rx.vstack(
        rx.heading("Catálogo de Libros"), 
        lista_libros,
        spacing="4",
    )