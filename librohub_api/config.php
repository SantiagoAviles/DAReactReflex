<?php
$host = "localhost";
$user = "root"; // Cambia si tu usuario de MySQL es distinto
$password = "admin"; // Cambia si tu MySQL tiene una contraseña
$dbname = "librohub";

$conn = new mysqli($host, $user, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>