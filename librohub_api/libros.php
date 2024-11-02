<?php
include 'config.php';

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE");

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'GET':
        $sql = "SELECT * FROM libros";
        $result = $conn->query($sql);
        $libros = [];

        while ($row = $result->fetch_assoc()) {
            $libros[] = $row;
        }
        echo json_encode($libros);
        break;

    case 'POST':
        $data = json_decode(file_get_contents("php://input"));
        $sql = "INSERT INTO libros (titulo, autor, isbn, genero, precio, descripcion) VALUES ('$data->titulo', '$data->autor', '$data->isbn', '$data->genero', '$data->precio', '$data->descripcion')";
        $conn->query($sql);
        echo json_encode(["message" => "Libro creado"]);
        break;

    case 'PUT':
        $data = json_decode(file_get_contents("php://input"));
        $id = $data->id;
        $sql = "UPDATE libros SET titulo='$data->titulo', autor='$data->autor', isbn='$data->isbn', genero='$data->genero', precio='$data->precio', descripcion='$data->descripcion' WHERE id=$id";
        $conn->query($sql);
        echo json_encode(["message" => "Libro actualizado"]);
        break;

    case 'DELETE':
        $id = $_GET['id'];
        $sql = "DELETE FROM libros WHERE id=$id";
        $conn->query($sql);
        echo json_encode(["message" => "Libro eliminado"]);
        break;
}
$conn->close();
?>
