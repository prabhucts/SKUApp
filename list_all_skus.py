#!/usr/bin/env python
# List all SKUs in the database

import sys
import sqlite3
import json
import argparse
from pathlib import Path

# Determine which database file to use
db_paths = [
    "skuapp.db",
    "backend/sku_database.db",
]

def find_db():
    for path in db_paths:
        if Path(path).exists():
            return path
    return None

def list_skus(db_path, status_filter=None, format_output="table"):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print(f"Connected to database: {db_path}")
        
        # Check if the skus table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='skus'")
        if cursor.fetchone():
            if status_filter:
                print(f"Fetching SKUs with status: {status_filter}...\n")
                cursor.execute(f"SELECT * FROM skus WHERE status LIKE ?", (f"%{status_filter}%",))
            else:
                print("Fetching all SKUs...\n")
                cursor.execute("SELECT * FROM skus")
                
            skus = [dict(row) for row in cursor.fetchall()]
        else:
            print("SKUs table not found. Available tables:")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            if tables:
                print(f"Tables found: {tables}")
                try:
                    cursor.execute(f"SELECT * FROM {tables[0]}")
                    skus = [dict(row) for row in cursor.fetchall()]
                except sqlite3.OperationalError as e:
                    print(f"Error querying table {tables[0]}: {str(e)}")
                    return
            else:
                print("No tables found in the database.")
                return
        
        # Print SKUs in the requested format
        print(f"Found {len(skus)} SKUs:")
        
        if format_output == "json":
            print(json.dumps(skus, indent=2))
        else:
            print("-" * 80)
            for sku in skus:
                print(f"SKU Number: {sku.get('skuNumber', 'N/A')}")
                print(f"NDC: {sku.get('ndc', 'N/A')}")
                print(f"Product Name: {sku.get('productName', 'N/A')}")
                print(f"Manufacturer: {sku.get('manufacturer', 'N/A')}")
                print(f"Dosage Form: {sku.get('form', 'N/A')}")
                print(f"Strength: {sku.get('strength', 'N/A')}")
                print(f"Package Size: {sku.get('packageSize', 'N/A')}")
                print(f"Status: {sku.get('status', 'N/A')}")
                print("-" * 80)
        
    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List SKUs from the database")
    parser.add_argument("--status", help="Filter SKUs by status (e.g., Active, Pending, Approved)")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format (default: table)")
    args = parser.parse_args()

    db_path = find_db()
    if not db_path:
        print("Error: Could not find database file.")
        sys.exit(1)
    
    list_skus(db_path, args.status, args.format)
