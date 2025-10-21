# Bug Fixes and Improvements - October 2025

## Issues Fixed

### 1. IndexError with Annotations
**Problem:** When deleting an annotation, the UI controls still referenced old indices, causing an `IndexError: list index out of range` when toggling annotations.

**Solution:** 
- Modified `_on_delete_annotation()` in `builder.py` to call `self.refresh()` after deleting an annotation
- This ensures the UI is rebuilt with correct indices

### 2. Dropdown UI Issues
**Problem:** Selected text in dropdowns was too far down to be visible, and dropdowns had insufficient height.

**Solution:**
- Increased dropdown height from 45-50px to 55-60px across all dropdowns
- Added `content_padding=ft.padding.symmetric(horizontal=10, vertical=8)` to all dropdowns for better text positioning
- Applied fixes to:
  - Chart Type dropdown
  - X Column dropdown  
  - Series Style dropdowns
  - Series Y Axis dropdowns
  - Scale dropdown (Axes section)
  - Legend dropdown
  - Theme Mode dropdown

### 3. Text Boxes Not Displaying Text
**Problem:** Some text fields didn't display their values properly.

**Solution:**
- Increased TextField height from 40px to 50px
- Added proper styling with:
  - `text_size=13`
  - `content_padding=ft.padding.symmetric(horizontal=10, vertical=10)`
  - Consistent background, text, and border colors
- Applied to:
  - Title field
  - Subtitle field
  - Y Axis Label field

### 4. Series Management - Add/Remove Functionality
**Problem:** Users couldn't add or remove data series, only toggle visibility.

**Solution:**
- Added "Add Series" button in the Series section
- Added delete icon button to each series control
- Implemented `_on_add_series()` method to add new series from available columns
- Implemented `_on_delete_series()` method to remove series
- Both operations properly refresh the UI to avoid index errors

### 5. State Management Improvements
**Problem:** Not all configuration changes were saving snapshots for undo/redo functionality.

**Solution:**
- Added `self.state.save_snapshot()` calls to all change handlers:
  - Chart type changes
  - X column changes
  - Series visibility/width/style/axis changes
  - Axes label/scale/grid changes
  - Title/subtitle/legend changes
  - Annotation toggles
  - Theme mode/font size changes

## Files Modified

1. **app/ui/builder.py**
   - Fixed annotation deletion with proper refresh
   - Improved all dropdown heights and padding
   - Improved all text field heights and styling
   - Added series add/remove functionality
   - Added save_snapshot to all change handlers

2. **app/main.py**
   - Updated `_on_config_change()` to remove redundant save_snapshot call (now handled by individual handlers)

## Testing

All fixes have been tested and the application runs without errors. The UI is now more user-friendly with:
- Properly visible dropdown selections
- Clear text field content
- Full control over data series (add/remove)
- No more index errors when deleting annotations or series
- Proper undo/redo state tracking for all changes

