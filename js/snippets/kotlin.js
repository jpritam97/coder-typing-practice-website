window.snippets = [
  'fun main() {\n    println("Hello, World!")\n}',
  'fun main() {\n    print("Enter your name: ")\n    val name = readLine()\n    println("Hello, $name!")\n}',
  'fun main() {\n    for (i in 0 until 5) {\n        println(i)\n    }\n}',
  'fun greet(name: String): String {\n    return "Hello, $name!"\n}\n\nfun main() {\n    val result = greet("Alice")\n    println(result)\n}',
  'fun main() {\n    val numbers = listOf(1, 2, 3, 4, 5)\n    val sum = numbers.sum()\n    println("Sum: $sum")\n}',
  'fun main() {\n    val age = 20\n    if (age >= 18) {\n        println("Adult")\n    } else {\n        println("Minor")\n    }\n}',
  'class Person(private val name: String) {\n    fun greet(): String {\n        return "Hello, I am $name"\n    }\n}\n\nfun main() {\n    val person = Person("Alice")\n    println(person.greet())\n}',
  'import kotlin.random.Random\n\nfun main() {\n    val randomNumber = Random.nextInt(1, 11)\n    println("Random number: $randomNumber")\n}'
]; 