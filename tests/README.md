# Tests - Module Kho Hàng

## 📋 Tổng quan

Bộ test suite cho module Quản lý Kho hàng (Phase 4).

---

## 🚀 Chạy Tests

### Chạy tất cả tests:
```bash
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python
pytest
```

### Chạy với coverage report:
```bash
pytest --cov=src --cov-report=html
```

### Chạy test cụ thể:
```bash
# Test KhoService
pytest tests/test_kho_service.py -v

# Test ViTriService
pytest tests/test_vi_tri_service.py -v

# Test specific function
pytest tests/test_kho_service.py::TestKhoServiceCreate::test_create_kho_success -v
```

### Chạy tests với markers:
```bash
# Bỏ qua tests chậm
pytest -m "not slow"

# Chỉ chạy integration tests
pytest -m integration
```

---

## 📁 Cấu trúc Tests

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures & config
├── test_kho_service.py      # Tests for KhoService (20+ tests)
├── test_vi_tri_service.py   # Tests for ViTriService (22+ tests)
└── README.md                # This file
```

---

## ✅ Test Coverage

### KhoService Tests (20 tests):
- ✅ Create (5 tests)
  - Test successful creation
  - Test auto-generate ma_kho
  - Test validation (missing fields, invalid values)
  
- ✅ Read (5 tests)
  - Test get_by_id
  - Test get_all with pagination
  - Test get_all with status filter
  - Test get_by_status
  
- ✅ Search (3 tests)
  - Test search by name
  - Test search by address
  - Test no results
  
- ✅ Update (2 tests)
  - Test successful update
  - Test update non-existent
  
- ✅ Delete (3 tests)
  - Test successful delete
  - Test delete non-existent
  - Test delete with positions
  
- ✅ Business Logic (2 tests)
  - Test calculate_fill_rate
  - Test get_available_capacity

### ViTriService Tests (22 tests):
- ✅ Create (6 tests)
  - Test successful creation
  - Test auto-generate ma_vi_tri
  - Test validation
  - Test kho not found
  
- ✅ Read (4 tests)
  - Test get_by_id
  - Test get_vi_tri_by_kho
  - Test get_all with pagination
  
- ✅ Search (2 tests)
  - Test search by khu_vuc
  - Test no results
  
- ✅ Update (2 tests)
  - Test successful update
  - Test update non-existent
  
- ✅ Delete (2 tests)
  - Test successful delete
  - Test delete non-existent
  
- ✅ Business Logic (4 tests)
  - Test get_available
  - Test get_statistics
  - Test update_status
  - Test find_available_by_requirements

---

## 📊 Coverage Report

Sau khi chạy `pytest --cov=src --cov-report=html`, mở file:
```
htmlcov/index.html
```

### Target Coverage:
- **Services:** > 80%
- **Models:** > 90%
- **Overall:** > 75%

---

## 🔧 Fixtures

### Available Fixtures:

**conftest.py:**
- `kho_service` - KhoService instance
- `vi_tri_service` - ViTriService instance
- `sample_kho` - Sample kho for testing
- `sample_vi_tri_data` - Sample vi_tri data
- `sample_kho_data` - Sample kho data dict

**Test Files:**
- Each test file has its own fixtures for cleanup

---

## 📝 Test Conventions

### Naming:
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Structure:
```python
class TestServiceName:
    """Test group for specific functionality"""
    
    def test_feature_success(self, fixture):
        """Test successful operation"""
        pass
    
    def test_feature_failure(self, fixture):
        """Test failure case"""
        pass
```

### Assertions:
- Use `assert` for all checks
- Use `pytest.raises()` for exceptions
- Provide clear error messages

---

## ⚠️ Notes

### Database:
- Tests currently use production database
- TODO: Setup separate test database or in-memory SQLite
- Fixtures handle cleanup after each test

### Slow Tests:
- Mark slow tests with `@pytest.mark.slow`
- Skip with `pytest -m "not slow"`

### Integration Tests:
- Mark with `@pytest.mark.integration`
- Require running database

---

## 🎯 Next Steps

### Phase 4 Testing:
- [ ] GUI tests (PyQt6)
- [ ] Integration tests (full workflow)
- [ ] Performance tests
- [ ] Mock external services

### Future:
- [ ] CI/CD integration (GitHub Actions)
- [ ] Automated coverage reporting
- [ ] Test database setup
- [ ] Fixture factories (factory_boy)

---

## 📚 Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Python testing best practices](https://docs.python-guide.org/writing/tests/)

---

**Updated:** 2026-04-23  
**Phase:** 4 (Kho Hàng)  
**Coverage Target:** > 80%
