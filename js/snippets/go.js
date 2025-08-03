window.snippets = [
  'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}',
  'package main\n\nimport "fmt"\n\nfunc main() {\n    var name string\n    fmt.Print("Enter your name: ")\n    fmt.Scanln(&name)\n    fmt.Printf("Hello, %s!\\n", name)\n}',
  'package main\n\nimport "fmt"\n\nfunc main() {\n    for i := 0; i < 5; i++ {\n        fmt.Println(i)\n    }\n}',
  'package main\n\nimport "fmt"\n\nfunc greet(name string) string {\n    return fmt.Sprintf("Hello, %s!", name)\n}\n\nfunc main() {\n    result := greet("Alice")\n    fmt.Println(result)\n}',
  'package main\n\nimport "fmt"\n\nfunc main() {\n    numbers := []int{1, 2, 3, 4, 5}\n    sum := 0\n    for _, num := range numbers {\n        sum += num\n    }\n    fmt.Printf("Sum: %d\\n", sum)\n}',
  'package main\n\nimport "fmt"\n\nfunc main() {\n    age := 20\n    if age >= 18 {\n        fmt.Println("Adult")\n    } else {\n        fmt.Println("Minor")\n    }\n}',
  'package main\n\nimport "fmt"\n\ntype Person struct {\n    name string\n}\n\nfunc (p Person) greet() string {\n    return fmt.Sprintf("Hello, I am %s", p.name)\n}\n\nfunc main() {\n    person := Person{name: "Alice"}\n    fmt.Println(person.greet())\n}',
  'package main\n\nimport (\n    "fmt"\n    "math/rand"\n    "time"\n)\n\nfunc main() {\n    rand.Seed(time.Now().UnixNano())\n    randomNumber := rand.Intn(10) + 1\n    fmt.Printf("Random number: %d\\n", randomNumber)\n}'
]; 