"""
Test script to verify deployment readiness
Run this before deploying to catch common issues
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")

    required_modules = [
        'pandas',
        'numpy',
        'plotly',
        'matplotlib',
        'sklearn',
        'requests',
        'bs4',
    ]

    optional_modules = [
        'openai',
        'langchain',
    ]

    failed = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - REQUIRED")
            failed.append(module)

    print("\nOptional modules (for AI features):")
    for module in optional_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"○ {module} - optional (needed for projects 3 & 8)")

    return len(failed) == 0

def test_file_structure():
    """Test if all required files exist"""
    print("\n\nTesting file structure...")

    required_files = [
        'Home.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'utils/__init__.py',
        'utils/styling.py',
        'utils/helpers.py',
    ]

    required_dirs = [
        'pages',
        'utils',
        '.streamlit',
    ]

    all_good = True

    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_good = False

    for dir in required_dirs:
        if os.path.isdir(dir):
            print(f"✓ {dir}/")
        else:
            print(f"✗ {dir}/ - MISSING")
            all_good = False

    # Count pages
    if os.path.isdir('pages'):
        pages = [f for f in os.listdir('pages') if f.endswith('.py')]
        print(f"\nFound {len(pages)} page files")
        for page in sorted(pages):
            print(f"  - {page}")

    return all_good

def test_syntax():
    """Test Python syntax of main files"""
    print("\n\nTesting Python syntax...")

    files_to_test = ['Home.py', 'utils/styling.py', 'utils/helpers.py']

    all_good = True
    for file in files_to_test:
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print(f"✓ {file}")
        except SyntaxError as e:
            print(f"✗ {file} - SYNTAX ERROR: {e}")
            all_good = False
        except Exception as e:
            print(f"○ {file} - Warning: {e}")

    return all_good

def main():
    print("=" * 60)
    print("STREAMLIT DEPLOYMENT READINESS TEST")
    print("=" * 60)

    imports_ok = test_imports()
    structure_ok = test_file_structure()
    syntax_ok = test_syntax()

    print("\n" + "=" * 60)
    if imports_ok and structure_ok and syntax_ok:
        print("✅ ALL TESTS PASSED - Ready for deployment!")
        print("\nNext steps:")
        print("1. Commit and push changes: git push origin main")
        print("2. Go to share.streamlit.io")
        print("3. Deploy with: Branch=main, File=Home.py")
    else:
        print("⚠️ SOME TESTS FAILED - Fix issues before deploying")
        if not imports_ok:
            print("\n  → Install missing packages: pip install -r requirements.txt")
        if not structure_ok:
            print("\n  → Ensure all files are committed")
        if not syntax_ok:
            print("\n  → Fix syntax errors in listed files")

    print("=" * 60)

if __name__ == "__main__":
    main()
