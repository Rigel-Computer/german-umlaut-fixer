#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_encoding.py - Python Script zum automatischen Reparieren von Encoding-Problemen
Bearbeitet alle Web-relevanten Dateien im aktuellen Verzeichnis und Unterverzeichnissen
Verwendung: python fix_encoding.py [--path VERZEICHNIS] [--dry-run]
"""

import os
import sys
import argparse
import shutil
from pathlib import Path

# Web-relevante Dateierweiterungen
WEB_EXTENSIONS = {'.php', '.html', '.htm', '.css', '.js', '.xml', '.json'}

# Encoding-Korrekturen definieren (von falsch zu richtig)
ENCODING_FIXES = {
    # Häufigste doppelte Encodings
    "ÃƒÂ¼": "ü",     # über, für, zurück
    "ÃƒÂ¤": "ä",     # wählen, später, erfüllt
    "ÃƒÂ¶": "ö",     # können, löschen
    "ÃƒÅ¸": "ß",     # Fußbereich (häufigste Variante)
    "ÃƒÅ¡": "ß",     # Alternative ß-Codierung
    "ÃƒÂ„": "Ä",     # Großes Ä
    "ÃƒÂ–": "Ö",     # Großes Ö
    "ÃƒÅ": "Ü",      # Großes Ü (wie VOLLSTÄNDIG)
    
    # Einfache Encodings  
    "Ã¼": "ü",       # für, über
    "Ã¤": "ä",       # später, wählen
    "Ã¶": "ö",       # können, löschen
    "ÃŸ": "ß",       # Fuß, Grüße
    "Ã„": "Ä",       # ÄNDERT
    "Ã–": "Ö",       # ÖFFNEN
    "Ãœ": "Ü",       # ÜBER
    
    # Spezielle Fälle aus den Dateien
    "spÃ¤ter": "später",           # häufig gesehen
    "mÃ¼ssen": "müssen",           # häufig gesehen  
    "fÃ¼r": "für",                 # sehr häufig
    "Ã¼ber": "über",               # sehr häufig
    "erfÃ¼llt": "erfüllt",         # passwort-bezogen
    "ausfÃ¼llen": "ausfüllen",     # formular-bezogen
    "zurÃ¼ck": "zurück",           # navigation
    "GrÃ¼ÃŸen": "Grüßen",         # e-mail signatur
    "bestÃ¤tigen": "bestätigen",   # bestätigung
    "UngÃ¼ltig": "Ungültig",       # validierung
    "gÃ¼ltig": "gültig",           # validierung
    "StÃ¤rke": "Stärke",           # passwort
    "GroÃŸbuchstabe": "Großbuchstabe",  # passwort
    "wÃ¤hlen": "wählen",           # select
    "BenÃ¶tigt": "Benötigt",       # javascript message
    "FunktionalitÃ¤t": "Funktionalität",  # javascript message
    "PersÃ¶nliche": "Persönliche", # form section
    "VOLLSTÃ„NDIG": "VOLLSTÄNDIG", # comments
    
    # Weitere häufige Web-Zeichen (mit Unicode-Escapes)
    "\u00e2\u201a\u00ac": "\u20ac",    # Euro-Symbol
    "\u00e2\u20ac\u0153": "\u201c",    # Anführungszeichen links
    "\u00e2\u20ac\ufffd": "\u201d",    # Anführungszeichen rechts  
    "\u00e2\u20ac\u2122": "\u2019",    # Apostroph
    "\u00e2\u20ac\u201c": "\u2013",    # En-Dash
    "\u00e2\u20ac\u201d": "\u2014",    # Em-Dash
    "\u00e2\u2020\u2019": "\u2190",    # Pfeil links
    "\u00e2\u2020\u2019": "\u2192",    # Pfeil rechts
}


class ColoredOutput:
    """Farbige Konsolen-Ausgabe für Windows und Unix"""
    
    def __init__(self):
        self.colors_enabled = self._check_color_support()
    
    def _check_color_support(self):
        """Prüft ob farbige Ausgabe unterstützt wird"""
        if os.name == 'nt':  # Windows
            try:
                # Windows 10 unterstützt ANSI Escape Codes
                os.system('color')
                return True
            except:
                return False
        else:  # Unix/Linux/Mac
            return True
    
    def colored(self, text, color):
        """Gibt farbigen Text zurück wenn unterstützt"""
        if not self.colors_enabled:
            return text
        
        colors = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'cyan': '\033[96m',
            'magenta': '\033[95m',
            'gray': '\033[90m',
            'reset': '\033[0m'
        }
        
        return f"{colors.get(color, '')}{text}{colors['reset']}"


def process_file(file_path, dry_run=False, output=None):
    """
    Verarbeitet eine einzelne Datei
    
    Args:
        file_path: Pfad zur Datei
        dry_run: Wenn True, werden keine Änderungen gespeichert
        output: ColoredOutput Instanz für farbige Ausgabe
        
    Returns:
        tuple: (anzahl_ersetzungen, datei_geändert)
    """
    try:
        # Verschiedene Encodings probieren
        content = None
        original_encoding = None
        
        for encoding in ['utf-8', 'windows-1252', 'iso-8859-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    original_encoding = encoding
                    break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"  {output.colored('✗ Konnte Datei nicht lesen (unbekanntes Encoding)', 'red')}")
            return 0, False
        
        original_content = content
        total_replacements = 0
        
        # Alle Encoding-Korrekturen anwenden
        for wrong, correct in ENCODING_FIXES.items():
            before_count = content.count(wrong)
            if before_count > 0:
                content = content.replace(wrong, correct)
                total_replacements += before_count
                print(f"  → {wrong} → {correct} ({before_count} mal)")
        
        # Datei schreiben falls Änderungen vorgenommen wurden
        if content != original_content:
            if not dry_run:
                # Backup erstellen
                backup_path = str(file_path) + '.backup'
                shutil.copy2(file_path, backup_path)
                
                # Reparierte Datei schreiben (immer als UTF-8)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  {output.colored('✓ Datei repariert', 'green')} ({total_replacements} Korrekturen)")
            else:
                print(f"  {output.colored('! Würde repariert werden', 'magenta')} ({total_replacements} Korrekturen)")
            
            return total_replacements, True
        
        return 0, False
        
    except Exception as e:
        print(f"  {output.colored(f'✗ Fehler: {e}', 'red')}")
        return 0, False


def main():
    """Hauptfunktion"""
    parser = argparse.ArgumentParser(
        description='Repariert Encoding-Probleme in Web-Dateien',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--path', 
        default='.', 
        help='Verzeichnis zum Durchsuchen (Standard: aktuelles Verzeichnis)'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Zeigt nur an, was geändert würde, ohne Dateien zu modifizieren'
    )
    
    args = parser.parse_args()
    
    output = ColoredOutput()
    
    print(output.colored("Encoding-Reparatur gestartet...", 'green'))
    print(f"Verzeichnis: {output.colored(args.path, 'cyan')}")
    print(f"Dry-Run Modus: {output.colored(str(args.dry_run), 'yellow')}")
    print()
    
    total_files = 0
    changed_files = 0
    total_replacements = 0
    
    # Durchsuche alle Web-relevanten Dateien
    search_path = Path(args.path)
    
    if not search_path.exists():
        print(output.colored(f"✗ Verzeichnis '{args.path}' existiert nicht!", 'red'))
        sys.exit(1)
    
    for file_path in search_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in WEB_EXTENSIONS:
            total_files += 1
            print(f"Prüfe: {output.colored(str(file_path), 'gray')}")
            
            replacements, changed = process_file(file_path, args.dry_run, output)
            total_replacements += replacements
            if changed:
                changed_files += 1
    
    # Zusammenfassung
    print()
    print(output.colored("=== ZUSAMMENFASSUNG ===", 'green'))
    print(f"Geprüfte Dateien: {output.colored(str(total_files), 'cyan')}")
    print(f"Geänderte Dateien: {output.colored(str(changed_files), 'yellow')}")
    print(f"Gesamte Korrekturen: {output.colored(str(total_replacements), 'green')}")
    
    if args.dry_run:
        print()
        print(output.colored("DRY-RUN: Keine Dateien wurden tatsächlich geändert.", 'magenta'))
        print(output.colored("Führe das Script ohne --dry-run aus, um Änderungen zu übernehmen.", 'magenta'))
    else:
        print()
        print(output.colored("Backups wurden als .backup-Dateien erstellt.", 'yellow'))
    
    print()
    print(output.colored("Fertig!", 'green'))


if __name__ == '__main__':
    main()
