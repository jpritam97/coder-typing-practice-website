window.snippets = [
  'console.log("Hello, World!");',
  'const name: string = prompt("Enter your name:") || "";\nconsole.log(`Hello, ${name}!`);',
  'for (let i = 0; i < 5; i++) {\n    console.log(i);\n}',
  'function greet(name: string): string {\n    return `Hello, ${name}!`;\n}\n\nconst result: string = greet("Alice");\nconsole.log(result);',
  'const numbers: number[] = [1, 2, 3, 4, 5];\nconst sum: number = numbers.reduce((a, b) => a + b, 0);\nconsole.log(`Sum: ${sum}`);',
  'const age: number = 20;\nif (age >= 18) {\n    console.log("Adult");\n} else {\n    console.log("Minor");\n}',
  'interface Person {\n    name: string;\n}\n\nclass PersonClass implements Person {\n    constructor(public name: string) {}\n    \n    greet(): string {\n        return `Hello, I am ${this.name}`;\n    }\n}\n\nconst person = new PersonClass("Alice");\nconsole.log(person.greet());',
  'const randomNumber: number = Math.floor(Math.random() * 10) + 1;\nconsole.log(`Random number: ${randomNumber}`);'
]; 