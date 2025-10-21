# Bug Fixes - October 2025

## Issues Fixed

### 1. AttributeError: 'NoneType' object has no attribute 'Figure'

**Error:**
```
File "/home/admin/Projects/graph-creator/app/charts/plotly_renderer.py", line 31, in PlotlyRenderer
  ) -> Tuple[go.Figure, Dict[str, Any]]:
         ^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'Figure'
```

**Root Cause:**
- When Plotly is not installed, the code sets `go = None` to handle import gracefully
- However, type annotations (like `go.Figure`) were evaluated at class definition time
- Python tried to access `go.Figure` when `go` was `None`, causing the crash

**Solution:**
- Added `from __future__ import annotations` to `app/charts/plotly_renderer.py`
- This enables PEP 563 (postponed evaluation of annotations)
- Type annotations are now treated as strings and not evaluated until needed at runtime
- The module can now import successfully whether Plotly is installed or not

**Files Changed:**
- `app/charts/plotly_renderer.py`

**Commit Details:**
```python
# Added at top of file:
from __future__ import annotations
```

---

### 2. AttributeError: module 'pandas' has no attribute 'np'

**Error:**
```
ERROR - Error loading example: module 'pandas' has no attribute 'np'
```

**Root Cause:**
- In pandas 2.0+, the `pd.np` alias for numpy was removed
- The code was using `pd.np.sin()` and `pd.np.cos()` which no longer exists
- This is a breaking change from pandas 1.x to 2.x

**Solution:**
- Added direct numpy import: `import numpy as np`
- Replaced all instances of `pd.np` with `np`
- Updated 6 occurrences across example data generation functions

**Files Changed:**
- `app/services/data_loader.py`

**Code Changes:**
```python
# Before:
'Metric A': 100 + pd.Series(range(100)) * 0.5 + pd.Series(range(100)).apply(lambda x: 10 * pd.np.sin(x / 10))

# After:
'Metric A': 100 + pd.Series(range(100)) * 0.5 + pd.Series(range(100)).apply(lambda x: 10 * np.sin(x / 10))
```

---

## Verification

All fixes have been verified:

✅ Application starts without errors
✅ Flet GUI loads successfully  
✅ Plotly renderer imports correctly (whether Plotly is installed or not)
✅ Example data generation works (using numpy functions)
✅ No linter errors introduced
✅ Type annotations working correctly

## Testing Commands

```bash
# Test application startup
cd /home/admin/Projects/graph-creator
source venv/bin/activate
python -m app.main

# Test data loader
python -c "from app.services.data_loader import DataLoader; ds = DataLoader.create_example_overlapping_trends(); print('✓ Success')"

# Test plotly renderer import
python -c "from app.charts.plotly_renderer import PlotlyRenderer; print('✓ Success')"
```

## Compatibility

**Current Versions:**
- Python: 3.11+ (tested on 3.12)
- pandas: 2.1.4 (2.x compatible)
- flet: 0.21.2
- matplotlib: 3.8.2
- numpy: 1.26.2

**Optional Dependencies:**
- plotly: 5.18.0 (optional, graceful fallback)
- kaleido: 0.2.1 (optional, for plotly export)

## Migration Notes

### For pandas 2.x compatibility:
- ❌ Don't use: `pd.np.*`
- ✅ Use instead: `import numpy as np` and use `np.*`

### For optional dependency type hints:
- ❌ Don't use: Type hints with conditionally imported modules
- ✅ Use instead: `from __future__ import annotations` to postpone evaluation

## Future Prevention

To prevent similar issues:

1. **Type Annotations**: Always use `from __future__ import annotations` when using optional dependencies in type hints
2. **pandas API**: Use direct numpy imports instead of `pd.np` alias
3. **Testing**: Test with both minimal and full dependency installations
4. **Documentation**: Keep track of breaking changes in major version updates

---

### 3. Title/Subtitle Overlapping in Chart Display

**Error:**
- Title and subtitle text overlapped when both were present
- Subtitle positioned too close to title causing readability issues

**Root Cause:**
- Title was positioned at y=0.98 and subtitle at y=0.96
- Insufficient padding between title and subtitle
- No alpha transparency for subtitle

**Solution:**
- Adjusted title position to y=1.02 when subtitle is present
- Increased padding to 30px when subtitle exists
- Added alpha=0.8 transparency to subtitle
- Adjusted subtitle y-position to 0.98
- Made subtitle font size slightly smaller (font_size - 1)

**Files Changed:**
- `app/charts/mpl_renderer.py`

---

### 4. Custom Dark/Light Mode Theme Implementation

**Request:**
- Implement custom dark mode theme as default
- Implement custom light mode theme
- Add theme toggle button
- Use specific color schemes provided by user

**Solution:**
Implemented complete custom theming system:

**Dark Mode Colors:**
- Background: #0C1A26 / #122738
- Accent: #3A82F7 / #4E9FB9
- Text: #E8EEF3 / #A5B3C0
- Success: #3DBE8B
- Warning: #E3A65A
- Error: #C05555

**Light Mode Colors:**
- Background: #F6F9FB / #E4EBF0
- Accent: #2F6BDB / #5FA7D3
- Text: #1E2B36 / #4B5E70
- Success: #2C8C64
- Warning: #C97A2C
- Error: #B23C3C

**Features Added:**
- Custom Flet theme with full color scheme
- Dark mode set as default
- Theme toggle button in header with icon
- Automatic chart re-rendering on theme change
- Matplotlib theme synchronization with UI theme

**Files Changed:**
- `app/main.py` - Added theme setup and toggle functionality
- `app/models/state.py` - Changed default theme to dark mode
- `app/ui/canvas.py` - Fixed image display issues (empty src_base64)

---

## All Fixes Summary

✅ **Issue 1:** Plotly import type annotation error - FIXED  
✅ **Issue 2:** pandas 2.x `pd.np` deprecation - FIXED  
✅ **Issue 3:** Title/subtitle text overlapping - FIXED  
✅ **Issue 4:** Custom dark/light theme - IMPLEMENTED  
✅ **Issue 5:** Theme toggle button - ADDED  
✅ **Issue 6:** Default dark mode - SET  
✅ **Issue 7:** Dropdown menu styling - IMPROVED  

---

**Fixed by:** AI Assistant  
**Date:** October 21, 2025  
**Status:** ✅ All issues resolved and features implemented

