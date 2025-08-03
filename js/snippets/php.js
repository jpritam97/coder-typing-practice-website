window.snippets = [
  '<?php\necho "Hello, World!";\n?>',
  '<?php\n$name = readline("Enter your name: ");\necho "Hello, $name!";\n?>',
  '<?php\nfor ($i = 0; $i < 5; $i++) {\n    echo $i . "\\n";\n}\n?>',
  '<?php\nfunction greet($name) {\n    return "Hello, $name!";\n}\n\n$result = greet("Alice");\necho $result;\n?>',
  '<?php\n$numbers = [1, 2, 3, 4, 5];\n$sum = array_sum($numbers);\necho "Sum: $sum";\n?>',
  '<?php\n$age = 20;\nif ($age >= 18) {\n    echo "Adult";\n} else {\n    echo "Minor";\n}\n?>',
  '<?php\nclass Person {\n    private $name;\n    \n    public function __construct($name) {\n        $this->name = $name;\n    }\n    \n    public function greet() {\n        return "Hello, I am " . $this->name;\n    }\n}\n\n$person = new Person("Alice");\necho $person->greet();\n?>',
  '<?php\n$randomNumber = rand(1, 10);\necho "Random number: $randomNumber";\n?>'
]; 