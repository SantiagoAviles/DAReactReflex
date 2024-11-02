import reflex as rx

@rx.page(route="/", title="LibroHub - Inicio")
def index():
    return rx.vstack(
        rx.heading("Bienvenido a LibroHub", font_size="3xl", color="white"),
        rx.text("Explora nuestra tienda de libros en línea.", font_size="lg", color="white"),
        rx.image(src="/static/images/welcome_image.png", width="300px", alt="Ilustración de libros"),
        rx.link(
            "Ir al catálogo",
            href="/catalogo",
            background_color="#6c63ff",
            color="white",
            padding="10px 20px",
            border_radius="5px",
            box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
            hover_background_color="#5a54e6",
            hover_box_shadow="0 6px 12px rgba(0, 0, 0, 0.3)",
            text_align="center",
            font_size="lg"
        ), spacing="4",
        style={
            "background": "linear-gradient(to right, #ff7e5f, #feb47b)", 
            "padding": "20px",
            "border_radius": "10px",
            "text_align": "center"
        }
    )