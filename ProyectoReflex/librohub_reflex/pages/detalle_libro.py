import reflex as rx
from ..app_state import LibroState 

@rx.page(route="/detalle-libro/[book_id]", title="Detalles del Libro")
def detalle_libro():
    try:
        book_id = int(rx.State.book_id)
        print(f"Book ID recibido: {book_id}") 
    except (ValueError, TypeError):
        book_id = None 

    detalles = LibroState.obtener_detalles_libro(book_id) if book_id else {
        "title_text": "Libro no encontrado",
        "author_text": "",
        "price_text": "",
        "stock": 0, 
        "image_path": ""
    }

    components = [
        rx.heading(detalles["title_text"]),
        rx.text(detalles["author_text"]), 
        rx.text(detalles["price_text"]),
        rx.text(f"Stock: {detalles['stock']}"), 
        rx.link("Volver al catálogo", href="/catalogo"), 
    ]

    if detalles["image_path"]:
        components.insert(1, rx.image(src=detalles["image_path"], alt="Imagen del Libro", width="200px"))

    return rx.vstack(*components,
        rx.input("Cantidad", type="number", min=1, on_change=LibroState.set_quantity),
        rx.cond(
            detalles["stock"] > 0, 
            rx.button("Comprar", on_click=lambda: LibroState.comprar_libro(book_id)),
            rx.text("No hay stock disponible"),
        ),
        spacing="4", 
    )