"""
Dialogs package - Dialog windows
"""
from .dialogs import (
    MessageDialog,
    ConfirmDialog,
    InputDialog,
    ProgressDialog,
    FormDialog,
)
from .change_password_dialog import ChangePasswordDialog

__all__ = [
    'MessageDialog',
    'ConfirmDialog',
    'InputDialog',
    'ProgressDialog',
    'FormDialog',
    'ChangePasswordDialog',
]
