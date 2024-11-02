import reflex as rx
from ..app_state import AdminState 

# Decorador que define la página de inicio de sesión para administradores
@rx.page(route="/login", title="Login Admin")
def login():
    # Retorna una estructura vertical que contiene el formulario de inicio de sesión
    return rx.vstack(
        rx.box(  # Contenedor para centrar el formulario
            rx.form(  # Formulario para el inicio de sesión
                rx.vstack(  # Disposición vertical de los elementos dentro del formulario
                    rx.heading("Login de Administrador", font_size="2xl", color="white"),  # Encabezado del formulario
                    rx.input("Usuario", on_change=AdminState.set_username, placeholder="Ingrese su usuario", 
                             border_radius="5px", padding="10px"),  # Campo para ingresar el nombre de usuario
                    rx.input("Contraseña", type="password", on_change=AdminState.set_password, 
                             placeholder="Ingrese su contraseña", border_radius="5px", padding="10px"),  # Campo para ingresar la contraseña
                    rx.button(  # Botón para iniciar sesión
                        "Iniciar sesión",
                        on_click=AdminState.login,  # Llama a la función de inicio de sesión al hacer clic
                        background_color="#6c63ff",  # Color de fondo del botón
                        color="white",  # Color del texto del botón
                        padding="10px 20px",  # Espaciado interno del botón
                        border_radius="5px",  # Bordes redondeados del botón
                        box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",  # Sombra del botón
                        hover_background_color="#5a54e6",  # Color de fondo al pasar el mouse sobre el botón
                        hover_box_shadow="0 6px 12px rgba(0, 0, 0, 0.3)",  # Sombra al pasar el mouse sobre el botón
                        font_size="lg"  # Tamaño de fuente del texto del botón
                    ),
                    rx.link("Regresar a index", href="/", color="#feb47b"),  # Enlace para regresar a la página principal
                    rx.cond(  # Condición que muestra un enlace o un mensaje según el estado de autenticación
                        AdminState.is_authenticated,
                        rx.link("Ir al panel de administración", href="/admin", color="#6c63ff"),  # Enlace al panel de administración si está autenticado
                        rx.text("Credenciales incorrectas.", color="red", font_weight="bold")  # Mensaje de error si las credenciales son incorrectas
                    )
                ),
                style={  # Estilo general del formulario
                    "background": "linear-gradient(to right, #ff7e5f, #feb47b)",  # Fondo con degradado
                    "padding": "20px",  # Espaciado interno del formulario
                    "border_radius": "10px",  # Bordes redondeados del formulario
                    "text_align": "center"  # Alineación centrada del texto en el formulario
                }
            ),
            width="400px", margin="auto", padding="20px", border_radius="10px", box_shadow="0 4px 20px rgba(0, 0, 0, 0.1)"  # Estilo del contenedor del formulario
        ),
        style={  # Estilo general de la página de inicio de sesión
            "background": "#f8f9fa", 
            "min_height": "100vh"  # Altura mínima para ocupar toda la pantalla
        }
    )