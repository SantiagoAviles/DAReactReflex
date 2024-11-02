import reflex as rx
from ..app_state import AdminState 

@rx.page(route="/login", title="Login Admin")
def login():
    return rx.vstack(
        rx.box(
            rx.form(
                rx.vstack(
                    rx.heading("Login de Administrador", font_size="2xl", color="white"),
                    rx.input("Usuario", on_change=AdminState.set_username, placeholder="Ingrese su usuario", 
                             border_radius="5px", padding="10px"),
                    rx.input("Contraseña", type="password", on_change=AdminState.set_password, 
                             placeholder="Ingrese su contraseña", border_radius="5px", padding="10px"),
                    rx.button(
                        "Iniciar sesión",
                        on_click=AdminState.login, background_color="#6c63ff", color="white", padding="10px 20px",
                        border_radius="5px", box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
                        hover_background_color="#5a54e6", hover_box_shadow="0 6px 12px rgba(0, 0, 0, 0.3)",
                        font_size="lg"
                    ),
                    rx.link("Regresar a index", href="/", color="#feb47b"),
                    rx.cond(
                        AdminState.is_authenticated,
                        rx.link("Ir al panel de administración", href="/admin", color="#6c63ff"),
                        rx.text("Credenciales incorrectas.", color="red", font_weight="bold")
                    )
                ),
                style={
                    "background": "linear-gradient(to right, #ff7e5f, #feb47b)", "padding": "20px", "border_radius": "10px", "text_align": "center"
                }
            ),width="400px", margin="auto", padding="20px", border_radius="10px",box_shadow="0 4px 20px rgba(0, 0, 0, 0.1)"
        ),
        style={
            "background": "#f8f9fa", "min_height": "100vh"
        }
    )