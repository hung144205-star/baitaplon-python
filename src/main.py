#!/usr/bin/env python3
"""
Quản Lý Kho Lưu trữ - Main Entry Point
Nhóm 12 - Lập trình Python

Usage:
    python main.py
    hoặc
    python src/main.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.app import main

if __name__ == "__main__":
    main()
