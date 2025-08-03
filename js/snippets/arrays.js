// js/snippets/arrays.js
window.snippets = [
  `int arr[3] = {1, 2, 3};\nstd::cout << arr[0];`,
  `int numbers[] = {10, 20, 30};\nfor(int i = 0; i < 3; i++) {\n  std::cout << numbers[i] << " ";\n}`,
  `int marks[5];\nmarks[0] = 90;\nmarks[1] = 85;\nstd::cout << "First mark: " << marks[0];`,
  `int data[4] = {1, 3, 5, 7};\nint sum = 0;\nfor(int i = 0; i < 4; i++) sum += data[i];\nstd::cout << "Sum: " << sum;`,
  `int matrix[2][2] = {{1, 2}, {3, 4}};\nstd::cout << matrix[1][0];`,
  `int a[] = {5, 10, 15};\nstd::cout << "Size: " << sizeof(a)/sizeof(a[0]);`,
  `std::string fruits[3] = {"Apple", "Banana", "Cherry"};\nfor (int i = 0; i < 3; i++) std::cout << fruits[i] << "\\n";`,
  `int even[5];\nfor (int i = 0; i < 5; i++) even[i] = i * 2;\nfor (int i = 0; i < 5; i++) std::cout << even[i] << " ";`,
  `int arr[] = {10, 20, 30, 40};\nint search = 30;\nbool found = false;\nfor (int i = 0; i < 4; i++) {\n  if (arr[i] == search) found = true;\n}\nstd::cout << (found ? "Found" : "Not Found");`,
  `int arr[] = {1, 2, 3, 4, 5};\nint max = arr[0];\nfor (int i = 1; i < 5; i++) if (arr[i] > max) max = arr[i];\nstd::cout << "Max: " << max;`,
  `int arr[2][3] = {{1, 2, 3}, {4, 5, 6}};\nfor (int i = 0; i < 2; i++) {\n  for (int j = 0; j < 3; j++) std::cout << arr[i][j] << " ";\n}`,
  `int arr[5] = {};\nfor (int i = 0; i < 5; i++) std::cin >> arr[i];\nfor (int i = 0; i < 5; i++) std::cout << arr[i] << " ";`,
  `char vowels[] = {'a', 'e', 'i', 'o', 'u'};\nfor (char v : vowels) std::cout << v << " ";`,
  `int arr[4] = {4, 3, 2, 1};\nstd::sort(arr, arr + 4);\nfor (int i : arr) std::cout << i << " ";`,
  `int a[] = {1, 2, 3};\nint b[] = {4, 5, 6};\nint c[3];\nfor (int i = 0; i < 3; i++) c[i] = a[i] + b[i];`,
  `int arr[] = {10, 20, 30};\nfor (int x : arr) std::cout << x << "\\n";`,
  `int arr[3][3];\nfor (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) arr[i][j] = i * j;`,
  `int arr[] = {4, 6, 8};\nstd::cout << "Middle: " << arr[1];`,
  `int size = 6;\nint arr[size] = {2, 4, 6, 8, 10, 12};\nfor (int i = 0; i < size; i++) std::cout << arr[i] << ",";`,
  `float scores[] = {88.5, 76.4, 90.2};\nfloat total = 0;\nfor (float s : scores) total += s;\nstd::cout << "Avg: " << total / 3;`
];

