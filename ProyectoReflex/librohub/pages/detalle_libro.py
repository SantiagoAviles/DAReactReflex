import reflex as rx
from ..app_state import LibroState 

# Decorador que define una nueva página en la aplicación para mostrar los detalles de un libro
@rx.page(route="/detalle-libro/[book_id]", title="Detalles del Libro")
def detalle_libro():
    try:
        # Intenta obtener el ID del libro desde el estado y convertirlo a entero
        book_id = int(rx.State.book_id)
        print(f"Book ID recibido: {book_id}")  # Imprime el ID del libro para depuración
    except (ValueError, TypeError):
        # Si ocurre un error al convertir el ID, se asigna None
        book_id = None 

    # Obtiene los detalles del libro a partir del ID o establece valores por defecto si no se encuentra
    detalles = LibroState.obtener_detalles_libro(book_id) if book_id else {
        "title_text": "Libro no encontrado",
        "author_text": "",
        "price_text": "",
        "stock": 0, 
        "image_path": ""
    }

    # Crea una lista de componentes para mostrar los detalles del libro
    components = [
        rx.heading(detalles["title_text"]),  # Título del libro
        rx.text(detalles["author_text"]),  # Autor del libro
        rx.text(detalles["price_text"]),  # Precio del libro
        rx.text(f"Stock: {detalles['stock']}"),  # Stock disponible del libro
        rx.link("Volver al catálogo", href="/catalogo"),  # Enlace para volver al catálogo de libros
    ]

    # Si hay una imagen disponible, se agrega al componente de detalles
    if detalles["image_path"]:
        components.insert(1, rx.image(src=detalles["image_path"], alt="Imagen del Libro", width="200px"))

    # Retorna la estructura de la página con los detalles del libro y un botón de compra si hay stock disponible
    return rx.vstack(*components,
        rx.input("Cantidad", type="number", min=1, on_change=LibroState.set_quantity),  # Campo para ingresar la cantidad a comprar
        rx.cond(
            detalles["stock"] > 0,  # Verifica si hay stock disponible
            rx.button("Comprar", on_click=lambda: LibroState.comprar_libro(book_id)),  # Botón para comprar el libro
            rx.text("No hay stock disponible"),  # Mensaje si no hay stock disponible
        ),
        spacing="4",  # Espaciado entre los elementos en la interfaz
    )