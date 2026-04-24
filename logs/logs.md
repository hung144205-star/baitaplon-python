(venv) hieu@home-lab:~/Documents/baitaplon/nhom12/hung/baitaplon-python$ python3 main_demo.py
Traceback (most recent call last):
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/src/gui/views/khach_hang_view.py", line 224, in _on_edit_clicked
    dialog = KhachHangForm(self, khach_hang=self.current_khach_hang)
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/src/gui/forms/khach_hang_form.py", line 40, in __init__
    self._load_data()
    ~~~~~~~~~~~~~~~^^
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/src/gui/forms/khach_hang_form.py", line 196, in _load_data
    self.loai_khach_input.setCurrentData(self.khach_hang.loai_khach.value, "")
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'QComboBox' object has no attribute 'setCurrentData'. Did you mean: 'currentData'?
Aborted (core dumped)

