window.snippets = [
  '#include <iostream>\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}',
  '#include <iostream>\n#include <string>\nint main() {\n    std::string name;\n    std::cout << "Enter your name: ";\n    std::cin >> name;\n    std::cout << "Hello, " << name << "!" << std::endl;\n    return 0;\n}',
  '#include <iostream>\nint main() {\n    for (int i = 0; i < 5; i++) {\n        std::cout << i << std::endl;\n    }\n    return 0;\n}',
  '#include <iostream>\n#include <string>\nstd::string greet(const std::string& name) {\n    return "Hello, " + name + "!";\n}\n\nint main() {\n    std::string result = greet("Alice");\n    std::cout << result << std::endl;\n    return 0;\n}',
  '#include <iostream>\n#include <vector>\nint main() {\n    std::vector<int> numbers = {1, 2, 3, 4, 5};\n    int sum = 0;\n    for (int num : numbers) {\n        sum += num;\n    }\n    std::cout << "Sum: " << sum << std::endl;\n    return 0;\n}',
  '#include <iostream>\nint main() {\n    int age = 20;\n    if (age >= 18) {\n        std::cout << "Adult" << std::endl;\n    } else {\n        std::cout << "Minor" << std::endl;\n    }\n    return 0;\n}',
  '#include <iostream>\n#include <string>\nclass Person {\nprivate:\n    std::string name;\npublic:\n    Person(const std::string& n) : name(n) {}\n    std::string greet() const {\n        return "Hello, I am " + name;\n    }\n};\n\nint main() {\n    Person person("Alice");\n    std::cout << person.greet() << std::endl;\n    return 0;\n}',
  '#include <iostream>\n#include <cstdlib>\n#include <ctime>\nint main() {\n    srand(time(0));\n    int randomNumber = rand() % 10 + 1;\n    std::cout << "Random number: " << randomNumber << std::endl;\n    return 0;\n}'
]; 