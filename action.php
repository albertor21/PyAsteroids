<?php
// define variables and set to empty values
$name = $email = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = test_input($_POST["name"]);
  $hiscore = test_input($_POST["score"]);
}

function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}



echo "<h2>Hi $name </h2>";
echo "<br>";
echo "<h2>you've got $hiscore points </h2>";
?>

