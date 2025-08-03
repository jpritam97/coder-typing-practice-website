window.snippets = [
  'Console.WriteLine("Hello, World!");',
  'Console.Write("Enter your name: ");\nstring name = Console.ReadLine();\nConsole.WriteLine($"Hello, {name}!");',
  'for (int i = 0; i < 5; i++)\n{\n    Console.WriteLine(i);\n}',
  'static string Greet(string name)\n{\n    return $"Hello, {name}!";\n}\n\nstring result = Greet("Alice");\nConsole.WriteLine(result);',
  'int[] numbers = { 1, 2, 3, 4, 5 };\nint sum = numbers.Sum();\nConsole.WriteLine($"Sum: {sum}");',
  'int age = 20;\nif (age >= 18)\n{\n    Console.WriteLine("Adult");\n}\nelse\n{\n    Console.WriteLine("Minor");\n}',
  'public class Person\n{\n    private string name;\n    \n    public Person(string name)\n    {\n        this.name = name;\n    }\n    \n    public string Greet()\n    {\n        return $"Hello, I am {name}";\n    }\n}',
  'Random random = new Random();\nint randomNumber = random.Next(1, 11);\nConsole.WriteLine($"Random number: {randomNumber}");'
]; 