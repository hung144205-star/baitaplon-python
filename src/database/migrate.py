#!/usr/bin/env python3
"""
Database migration script
Hỗ trợ tạo migrations và áp dụng changes vào database

Usage:
    python -m src.database.migrate init    # Initialize migrations
    python -m src.database.migrate create  # Create new migration
    python -m src.database.migrate upgrade # Apply migrations
    python -m src.database.migrate status  # Show migration status
"""
import sys
import os
import shutil
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

MIGRATIONS_DIR = os.path.join(project_root, 'migrations')
DATA_DIR = os.path.join(project_root, 'data')
DB_PATH = os.path.join(DATA_DIR, 'warehouse.db')

def init_migrations():
    """Initialize migrations directory"""
    print("📦 Initializing migrations directory...")
    
    if not os.path.exists(MIGRATIONS_DIR):
        os.makedirs(MIGRATIONS_DIR)
        print(f"✅ Created migrations directory: {MIGRATIONS_DIR}")
    
    # Create versions directory
    versions_dir = os.path.join(MIGRATIONS_DIR, 'versions')
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)
        print(f"✅ Created versions directory: {versions_dir}")
    
    # Create migration script template
    template = '''"""
Migration script
Created: {timestamp}
"""
from sqlalchemy import text

def upgrade(connection):
    """
    Apply migration
    """
    # Example:
    # connection.execute(text("ALTER TABLE khach_hang ADD COLUMN ghi_chu TEXT"))
    pass

def downgrade(connection):
    """
    Rollback migration
    """
    # Example:
    # connection.execute(text("ALTER TABLE khach_hang DROP COLUMN ghi_chu"))
    pass
'''.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    template_file = os.path.join(MIGRATIONS_DIR, 'template.py')
    with open(template_file, 'w') as f:
        f.write(template)
    print(f"✅ Created migration template: {template_file}")
    
    # Create migrations log file
    log_file = os.path.join(MIGRATIONS_DIR, 'migrations.log')
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write("# Migrations Log\n")
            f.write("# Format: timestamp | migration_file | status\n")
        print(f"✅ Created migrations log: {log_file}")
    
    print("\n✅ Migrations initialized successfully!")

def create_migration(name="migration"):
    """Create a new migration file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{name}.py"
    
    versions_dir = os.path.join(MIGRATIONS_DIR, 'versions')
    if not os.path.exists(versions_dir):
        print("❌ Migrations not initialized. Run 'init' first.")
        return
    
    filepath = os.path.join(versions_dir, filename)
    
    template = '''"""
Migration: {name}
Created: {timestamp}
"""
from sqlalchemy import text

def upgrade(connection):
    """
    Apply migration
    Add your upgrade SQL here
    """
    print("Applying migration: {name}")
    # Example:
    # connection.execute(text("ALTER TABLE table_name ADD COLUMN column_name TYPE"))
    pass

def downgrade(connection):
    """
    Rollback migration
    Add your downgrade SQL here
    """
    print("Rolling back migration: {name}")
    # Example:
    # connection.execute(text("ALTER TABLE table_name DROP COLUMN column_name"))
    pass
'''.format(name=name, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    with open(filepath, 'w') as f:
        f.write(template)
    
    print(f"✅ Created migration: {filepath}")
    print(f"📝 Edit this file to add your migration logic")

def upgrade():
    """Apply all pending migrations"""
    print("🔄 Applying migrations...")
    
    if not os.path.exists(DB_PATH):
        print("❌ Database not found. Run init_db first.")
        return
    
    versions_dir = os.path.join(MIGRATIONS_DIR, 'versions')
    if not os.path.exists(versions_dir):
        print("❌ No migrations found. Run 'init' first.")
        return
    
    # Get list of migration files
    migration_files = sorted([f for f in os.listdir(versions_dir) if f.endswith('.py') and not f.startswith('_')])
    
    if not migration_files:
        print("✅ No migrations to apply")
        return
    
    # Import and run migrations
    from src.database.connection import get_engine
    
    engine = get_engine()
    
    with engine.connect() as connection:
        for migration_file in migration_files:
            filepath = os.path.join(versions_dir, migration_file)
            print(f"📄 Applying migration: {migration_file}")
            
            try:
                # Import migration module
                import importlib.util
                spec = importlib.util.spec_from_file_location("migration", filepath)
                migration = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(migration)
                
                # Run upgrade
                if hasattr(migration, 'upgrade'):
                    migration.upgrade(connection)
                    connection.commit()
                    print(f"✅ Applied: {migration_file}")
                else:
                    print(f"⚠️  No upgrade function in {migration_file}")
                    
            except Exception as e:
                print(f"❌ Error applying {migration_file}: {e}")
                connection.rollback()
                break
    
    print("\n✅ Migrations applied successfully!")

def status():
    """Show migration status"""
    print("📊 Migration Status\n")
    
    if not os.path.exists(MIGRATIONS_DIR):
        print("❌ Migrations not initialized")
        return
    
    versions_dir = os.path.join(MIGRATIONS_DIR, 'versions')
    if os.path.exists(versions_dir):
        migration_files = sorted([f for f in os.listdir(versions_dir) if f.endswith('.py') and not f.startswith('_')])
        
        if migration_files:
            print(f"📁 Migrations directory: {versions_dir}")
            print(f"📄 Found {len(migration_files)} migration(s):\n")
            
            for i, filename in enumerate(migration_files, 1):
                filepath = os.path.join(versions_dir, filename)
                size = os.path.getsize(filepath)
                print(f"  {i}. {filename} ({size} bytes)")
        else:
            print("📄 No migrations yet")
    else:
        print("❌ No versions directory")
    
    print(f"\n💾 Database: {DB_PATH}")
    if os.path.exists(DB_PATH):
        size = os.path.getsize(DB_PATH)
        print(f"   Size: {size:,} bytes")
    else:
        print("   Status: Not created")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    
    if command == 'init':
        init_migrations()
    elif command == 'create':
        name = sys.argv[2] if len(sys.argv) > 2 else "migration"
        create_migration(name)
    elif command == 'upgrade':
        upgrade()
    elif command == 'status':
        status()
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
