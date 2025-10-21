"""Dialog components."""

import flet as ft
from typing import Optional, Callable


class FilePickerDialog:
    """File picker dialog helper."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.on_result: Optional[Callable] = None
        
        self.file_picker = ft.FilePicker(
            on_result=self._handle_result,
        )
        
        page.overlay.append(self.file_picker)
    
    def pick_file(self, allowed_extensions: list, on_result: Callable):
        """Show file picker."""
        self.on_result = on_result
        self.file_picker.pick_files(
            allowed_extensions=allowed_extensions,
            allow_multiple=False,
        )
    
    def save_file(self, file_name: str, on_result: Callable):
        """Show save file dialog."""
        self.on_result = on_result
        self.file_picker.save_file(
            file_name=file_name,
        )
    
    def _handle_result(self, e: ft.FilePickerResultEvent):
        """Handle file picker result."""
        if self.on_result:
            self.on_result(e)


class TextInputDialog(ft.AlertDialog):
    """Simple text input dialog."""
    
    def __init__(
        self,
        title: str,
        label: str,
        on_submit: Callable,
        multiline: bool = False,
        **kwargs
    ):
        self.text_field = ft.TextField(
            label=label,
            multiline=multiline,
            min_lines=5 if multiline else 1,
            max_lines=10 if multiline else 1,
        )
        
        super().__init__(
            title=ft.Text(title),
            content=self.text_field,
            actions=[
                ft.TextButton("Cancel", on_click=self._on_cancel),
                ft.TextButton("OK", on_click=lambda e: self._on_ok(e, on_submit)),
            ],
            **kwargs
        )
    
    def _on_cancel(self, e):
        """Handle cancel."""
        self.open = False
        if hasattr(self, 'page') and self.page:
            self.page.update()
    
    def _on_ok(self, e, on_submit: Callable):
        """Handle OK."""
        value = self.text_field.value
        self.open = False
        if hasattr(self, 'page') and self.page:
            self.page.update()
        on_submit(value)


class ErrorDialog(ft.AlertDialog):
    """Error message dialog."""
    
    def __init__(self, title: str, message: str, **kwargs):
        super().__init__(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=self._on_ok),
            ],
            **kwargs
        )
    
    def _on_ok(self, e):
        """Handle OK."""
        self.open = False
        if hasattr(self, 'page') and self.page:
            self.page.update()


class SuccessDialog(ft.AlertDialog):
    """Success message dialog."""
    
    def __init__(self, title: str, message: str, **kwargs):
        super().__init__(
            title=ft.Text(title),
            content=ft.Text(message),
            icon=ft.icons.CHECK_CIRCLE,
            actions=[
                ft.TextButton("OK", on_click=self._on_ok),
            ],
            **kwargs
        )
    
    def _on_ok(self, e):
        """Handle OK."""
        self.open = False
        if hasattr(self, 'page') and self.page:
            self.page.update()

