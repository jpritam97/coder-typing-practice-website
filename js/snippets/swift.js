window.snippets = [
  'print("Hello, World!")',
  'print("Enter your name: ", terminator: "")\nif let name = readLine() {\n    print("Hello, \\(name)!")\n}',
  'for i in 0..<5 {\n    print(i)\n}',
  'func greet(name: String) -> String {\n    return "Hello, \\(name)!"\n}\n\nlet result = greet(name: "Alice")\nprint(result)',
  'let numbers = [1, 2, 3, 4, 5]\nlet sum = numbers.reduce(0, +)\nprint("Sum: \\(sum)")',
  'let age = 20\nif age >= 18 {\n    print("Adult")\n} else {\n    print("Minor")\n}',
  'class Person {\n    private let name: String\n    \n    init(name: String) {\n        self.name = name\n    }\n    \n    func greet() -> String {\n        return "Hello, I am \\(name)"\n    }\n}\n\nlet person = Person(name: "Alice")\nprint(person.greet())',
  'let randomNumber = Int.random(in: 1...10)\nprint("Random number: \\(randomNumber)")'
]; 