import reflex as rx

# Decorador que define la página principal de la aplicación
@rx.page(route="/", title="LibroHub - Inicio")
def index():
    # Retorna una estructura vertical con varios componentes para la página de inicio
    return rx.vstack(
        rx.heading("Bienvenido a LibroHub", font_size="3xl", color="white"),  # Encabezado principal
        rx.text("Explora nuestra tienda de libros en línea.", font_size="lg", color="white"),  # Texto introductorio
        rx.image(src="/static/images/welcome_image.png", width="300px", alt="Ilustración de libros"),  # Imagen de bienvenida
        rx.link(  # Enlace que lleva al catálogo de libros
            "Ir al catálogo",
            href="/catalogo",
            background_color="#6c63ff",  # Color de fondo del enlace
            color="white",  # Color del texto del enlace
            padding="10px 20px",  # Espaciado interno del enlace
            border_radius="5px",  # Bordes redondeados del enlace
            box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",  # Sombra del enlace
            hover_background_color="#5a54e6",  # Color de fondo al pasar el mouse
            hover_box_shadow="0 6px 12px rgba(0, 0, 0, 0.3)",  # Sombra al pasar el mouse
            text_align="center",  # Alineación del texto en el centro
            font_size="lg"  # Tamaño de fuente del texto del enlace
        ), spacing="4",  # Espaciado entre los elementos dentro del contenedor vertical
        style={  # Estilo general del contenedor vertical
            "background": "linear-gradient(to right, #ff7e5f, #feb47b)",  # Fondo con degradado
            "padding": "20px",  # Espaciado interno del contenedor
            "border_radius": "10px",  # Bordes redondeados del contenedor
            "text_align": "center"  # Alineación del texto en el centro
        }
    )