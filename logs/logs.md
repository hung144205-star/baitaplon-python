(venv) hieu@home-lab:~/Documents/baitaplon/nhom12/hung/baitaplon-python$ python main.py
Traceback (most recent call last):
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/src/gui/views/kho_view.py", line 265, in _on_edit_clicked
    dialog = KhoForm(self, kho=self.current_kho)
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/src/gui/forms/kho_form.py", line 35, in __init__
    self.load_data()
    ~~~~~~~~~~~~~~^^
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/src/gui/forms/kho_form.py", line 252, in load_data
    if self.kho.ghi_chu:
       ^^^^^^^^^^^^^^^^
AttributeError: 'Kho' object has no attribute 'ghi_chu'
Aborted (core dumped)

