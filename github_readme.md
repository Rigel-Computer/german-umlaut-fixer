# 🇩🇪 German Umlaut Fixer

**A Python script to automatically repair corrupted German umlauts (ä, ö, ü, ß) in web files caused by encoding issues.**

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg)]()

## 🚀 Quick Start

```bash
# Preview changes (safe)
python fix_encoding.py --dry-run

# Fix all files (creates backups)
python fix_encoding.py

# Fix specific directory
python fix_encoding.py --path "/path/to/project" --dry-run
```

## ⚡ What It Fixes

Transforms broken German characters back to proper UTF-8:

```
❌ fÃ¼r        → ✅ für
❌ spÃ¤ter      → ✅ später  
❌ VOLLSTÃ„NDIG → ✅ VOLLSTÄNDIG
❌ Ã¼ber       → ✅ über
❌ GrÃ¼ÃŸen    → ✅ Grüßen
```

## 🎯 The Problem

German websites often suffer from encoding corruption when migrating between systems or mixing UTF-8 with Windows-1252/ISO-8859-1. This script automatically detects and fixes the most common German encoding issues in web files.

## ✨ Features

- 🛡️ **Safe**: Creates automatic backups before any changes
- 🧪 **Preview Mode**: `--dry-run` shows changes without modifying files
- 🎯 **Smart Detection**: Only processes web files (.php, .html, .css, .js, .xml, .json)
- 🔍 **Multi-Encoding**: Handles UTF-8, Windows-1252, ISO-8859-1 input files
- 🎨 **Visual Feedback**: Colored output shows exactly what gets fixed
- 📦 **Zero Dependencies**: Uses only Python standard library
- 🌍 **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

- **Python 3.6 or higher**
- **Required libraries** (all part of Python standard library):
  - `os` - Operating system functions
  - `sys` - System-specific parameters
  - `argparse` - Command-line argument parsing
  - `shutil` - File operations
  - `pathlib` - Path operations

**🔍 Auto-Check Feature:** The script automatically verifies all dependencies and Python version compatibility on startup. If anything is missing, you'll get a clear error message with instructions on how to fix it.

*No pip installs, no external dependencies, no hassle!*

## 📁 Repository Structure

```
german-umlaut-fixer/
├── fix_encoding.py           # Main script
├── README.md                 # This file
├── README_DE.md              # German documentation
├── examples/
│   ├── before.html          # Example with broken umlauts
│   └── after.html           # Fixed version
└── docs/
    └── medium-article.md    # Detailed explanation (German)
```

## 🔧 Usage Examples

### Basic Usage
```bash
# Check what would be fixed
python fix_encoding.py --dry-run

# Fix files in current directory
python fix_encoding.py
```

### Advanced Usage
```bash
# Fix specific project directory
python fix_encoding.py --path "/var/www/german-site" --dry-run
python fix_encoding.py --path "/var/www/german-site"

# WordPress theme example
cd wp-content/themes/german-theme
python fix_encoding.py --dry-run
```

### Sample Output
```
==================================================
     German Encoding Repair Tool v1.0
==================================================

Checking: kontakt.php
  → fÃ¼r → für (5 times)
  → spÃ¤ter → später (2 times)  
  ✓ File repaired (7 corrections)

=== SUMMARY ===
Files checked: 23
Files changed: 8
Total corrections: 47

Backups created as .backup files.
```

## 🛡️ Safety & Recovery

**Always create backups first!** The script automatically creates `.backup` files, but you should also backup your entire project.

### Restore from backups:
```bash
# Single file
cp file.php.backup file.php

# All files (Linux/Mac)
for backup in *.backup; do cp "$backup" "${backup%.backup}"; done
```

## 🎯 Common Use Cases

- **Legacy Website Migration**: Fix encoding issues from old German CMS systems
- **Database Export Cleanup**: Repair corrupted German text in SQL dumps  
- **WordPress German Sites**: Clean up theme and content encoding problems
- **Corporate German Websites**: Fix encoding issues from mixed hosting environments

## 🔍 Technical Details

### Supported Input Encodings
- UTF-8 (with/without BOM)
- Windows-1252 (Western European)
- ISO-8859-1 (Latin-1)
- CP1252 (Windows Western European)

### File Types Processed
- `.php` - PHP files
- `.html`, `.htm` - HTML files  
- `.css` - Stylesheets
- `.js` - JavaScript files
- `.xml` - XML files
- `.json` - JSON files

### Output
- Always UTF-8 without BOM
- Preserves file structure and permissions
- Creates `.backup` files for safety

## ⚠️ Important Warnings

- **USE AT YOUR OWN RISK** - Always test with `--dry-run` first
- **BACKUP YOUR DATA** - While the script creates backups, have your own backup strategy
- **TEST THOROUGHLY** - Review results before deleting backup files
- **EDGE CASES** - The script handles 95% of German encoding issues, but complex cases may need manual review

## 🤝 Contributing

Found a German encoding pattern that's not covered? Please open an issue with:
- The corrupted text example
- The expected correct text
- Context (file type, source system)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🏷️ Repository Name Suggestion

**Repo Name**: `german-umlaut-fixer`

**Alternative Names**:
- `umlaut-repair-tool`
- `german-encoding-fixer` 
- `utf8-umlaut-cleaner`

---

*This tool was specifically created to solve the common German web development problem of corrupted umlauts due to encoding mismatches between UTF-8 and legacy Windows-1252 systems.*