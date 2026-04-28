#!/usr/bin/env python3
"""
Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa
Nhóm 12 - Lập trình Python

Usage:
    python main.py
"""
import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# Import main application
from src.main_app import main

if __name__ == "__main__":
    main()