window.snippets = [
  'fn main() {\n    println!("Hello, World!");\n}',
  'use std::io;\n\nfn main() {\n    println!("Enter your name: ");\n    let mut name = String::new();\n    io::stdin().read_line(&mut name).unwrap();\n    println!("Hello, {}!", name.trim());\n}',
  'fn main() {\n    for i in 0..5 {\n        println!("{}", i);\n    }\n}',
  'fn greet(name: &str) -> String {\n    format!("Hello, {}!", name)\n}\n\nfn main() {\n    let result = greet("Alice");\n    println!("{}", result);\n}',
  'fn main() {\n    let numbers = vec![1, 2, 3, 4, 5];\n    let sum: i32 = numbers.iter().sum();\n    println!("Sum: {}", sum);\n}',
  'fn main() {\n    let age = 20;\n    if age >= 18 {\n        println!("Adult");\n    } else {\n        println!("Minor");\n    }\n}',
  'struct Person {\n    name: String,\n}\n\nimpl Person {\n    fn new(name: &str) -> Person {\n        Person {\n            name: name.to_string(),\n        }\n    }\n    \n    fn greet(&self) -> String {\n        format!("Hello, I am {}", self.name)\n    }\n}\n\nfn main() {\n    let person = Person::new("Alice");\n    println!("{}", person.greet());\n}',
  'use rand::Rng;\n\nfn main() {\n    let mut rng = rand::thread_rng();\n    let random_number: u32 = rng.gen_range(1..=10);\n    println!("Random number: {}", random_number);\n}'
]; 