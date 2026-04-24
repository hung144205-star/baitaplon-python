venv) hieu@home-lab:~/Documents/baitaplon/nhom12/hung/baitaplon-python$ python main.py
Traceback (most recent call last):
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/main.py", line 176, in <module>
    main()
    ~~~~^^
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/main.py", line 169, in main
    window = MainWindow()
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/main.py", line 38, in __init__
    self.setup_ui()
    ~~~~~~~~~~~~~^^
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/main.py", line 103, in setup_ui
    self.add_module_tabs()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/main.py", line 122, in add_module_tabs
    vi_tri_view = ViTriView()
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/src/gui/views/vi_tri_view.py", line 39, in __init__
    self.setup_connections()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python/src/gui/views/vi_tri_view.py", line 212, in setup_connections
    self.table_with_toolbar.toolbar.export_clicked.connect(self._on_export_clicked)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'QWidget' object has no attribute 'export_clicked'

