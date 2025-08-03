#!/usr/bin/env python3
"""
Snippet Management Utility
Add new code snippets to language files easily.
"""

import os
import sys

# Available languages and their files
LANGUAGES = {
    'python': 'python_snippets.txt',
    'javascript': 'javascript_snippets.txt',
    'java': 'java_snippets.txt',
    'cpp': 'cpp_snippets.txt',
    'csharp': 'csharp_snippets.txt',
    'php': 'php_snippets.txt',
    'ruby': 'ruby_snippets.txt',
    'go': 'go_snippets.txt',
    'rust': 'rust_snippets.txt',
    'swift': 'swift_snippets.txt',
    'kotlin': 'kotlin_snippets.txt',
    'typescript': 'typescript_snippets.txt'
}

def list_languages():
    """List all available languages and their snippet counts"""
    print("📚 Available Languages:")
    print("-" * 50)
    
    for lang, filename in LANGUAGES.items():
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                snippets = [s.strip() for s in content.split('\n\n') if s.strip()]
                count = len(snippets)
                print(f"✅ {lang.title():12} - {count:3d} snippets ({filename})")
        else:
            print(f"❌ {lang.title():12} - No file found ({filename})")

def add_snippet(language, snippet):
    """Add a new snippet to the specified language file"""
    if language not in LANGUAGES:
        print(f"❌ Language '{language}' not supported")
        print(f"Available languages: {', '.join(LANGUAGES.keys())}")
        return False
    
    filename = LANGUAGES[language]
    
    # Create file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            pass
        print(f"📄 Created new file: {filename}")
    
    # Add snippet to file
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"\n\n{snippet}")
    
    print(f"✅ Added snippet to {language} ({filename})")
    return True

def interactive_add():
    """Interactive mode to add snippets"""
    print("🎯 Interactive Snippet Addition")
    print("=" * 50)
    
    # Show available languages
    list_languages()
    print()
    
    # Get language choice
    while True:
        language = input("Enter language (or 'list' to see languages): ").lower().strip()
        if language == 'list':
            list_languages()
            print()
            continue
        elif language in LANGUAGES:
            break
        else:
            print(f"❌ Language '{language}' not supported")
            print(f"Available languages: {', '.join(LANGUAGES.keys())}")
    
    # Get snippet
    print(f"\n📝 Adding snippet for {language.title()}")
    print("Enter your code snippet (press Enter twice to finish):")
    
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    
    # Remove the last empty line
    if lines and lines[-1] == "":
        lines.pop()
    
    snippet = '\n'.join(lines)
    
    if snippet.strip():
        if add_snippet(language, snippet):
            print(f"\n🎉 Snippet added successfully to {language}!")
        else:
            print("\n❌ Failed to add snippet")
    else:
        print("\n❌ No snippet provided")

def main():
    """Main function"""
    print("🚀 Snippet Management Utility")
    print("=" * 50)
    
    if len(sys.argv) == 1:
        # Interactive mode
        interactive_add()
    elif len(sys.argv) == 2 and sys.argv[1] == 'list':
        # List languages
        list_languages()
    elif len(sys.argv) >= 3:
        # Command line mode: python add_snippet.py <language> <snippet>
        language = sys.argv[1].lower()
        snippet = ' '.join(sys.argv[2:])
        
        if add_snippet(language, snippet):
            print(f"🎉 Snippet added successfully to {language}!")
        else:
            sys.exit(1)
    else:
        print("Usage:")
        print("  python add_snippet.py                    # Interactive mode")
        print("  python add_snippet.py list               # List all languages")
        print("  python add_snippet.py python 'print(\"Hello\")'  # Add snippet")
        print()
        print("Examples:")
        print("  python add_snippet.py python 'print(\"Hello, World!\")'")
        print("  python add_snippet.py javascript 'console.log(\"Hello\");'")
        print("  python add_snippet.py java 'System.out.println(\"Hello\");'")

if __name__ == '__main__':
    main() 