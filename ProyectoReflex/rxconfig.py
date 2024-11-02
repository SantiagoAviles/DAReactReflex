# Importamos la biblioteca reflex
import reflex as rx

# Configuramos la aplicación Reflex
config = rx.Config(
    app_name="librohub",  # Nombre de la aplicación que se mostrará
    db_url="mysql+mysqlconnector://admin:root@localhost/librohub_db",  # URL de conexión a la base de datos MySQL
    debug=True,  # Activamos el modo de depuración para facilitar el desarrollo
)