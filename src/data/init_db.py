#!/usr/bin/env python3
"""
Script khởi tạo database
Chạy script này để tạo database, tables, indexes, views và dữ liệu mẫu

Usage:
    python -m src.data.init_db
    hoặc
    python src/data/init_db.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.data.database import main

if __name__ == "__main__":
    main()
