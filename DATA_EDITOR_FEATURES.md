# Data Editor - Complete Real-Time Data Control

## Overview
The Graph Creator now includes a **full-featured data editor** that allows you to customize all data in real-time, with immediate graph updates!

---

## ✨ New Features

### 1. **Editable Data Table**
- Click on any cell to edit its value
- Type new values and press Enter or click away to save
- Changes update the graph **instantly**
- Automatic type conversion (numbers, strings)
- Supports up to 10 rows × 6 columns visible (with scrolling for more)

### 2. **Row Operations**
- **Add Row**: Adds a new row with default values (0 for numbers, empty for text)
- **Delete Last Row**: Removes the last row from the dataset
- Real-time graph updates after each operation

### 3. **Column Operations**
- **Add Column**: Creates a new column named "NewColumn" (or NewColumn1, NewColumn2, etc.)
- **Delete Column**: Click the delete icon in the column header
- **Rename Column**: Click on column name, edit it, press Enter
  - Automatically updates all series using that column
  - Updates X-axis selection if renamed
  - Prevents duplicate column names

### 4. **Export Functionality**
- **Export CSV**: Export your edited data as a CSV file
- Preserves all your manual edits
- Available directly from the Data Editor

---

## 🎯 How to Use

### Editing Cell Values

1. Expand the **"Data Editor"** section
2. Click on any cell in the table
3. Type a new value
4. Press **Enter** or click outside the cell
5. Watch the graph update instantly! 📊

**Examples:**
- Change `100` to `150` → Line moves up
- Change `5.5` to `3.2` → Point adjusts
- Modify any data point → See real-time changes

### Adding Data

**Add a Row:**
1. Click **"Add Row"** button
2. New row appears with default values
3. Edit the new cells as needed
4. Graph extends to include new data point

**Add a Column:**
1. Click **"Add Column"** button
2. New column named "NewColumn" appears
3. Rename it by clicking the column header
4. Edit cell values
5. Add it as a series in the "Series" section

### Deleting Data

**Delete a Row:**
1. Click **"Delete Last Row"** button
2. Last row is removed
3. Graph updates to exclude that data point

**Delete a Column:**
1. Click the delete icon (🗑️) in the column header
2. Column is removed
3. Any series using that column are removed
4. Graph updates automatically

### Renaming Columns

1. Click on the column name in the header
2. Type the new name
3. Press **Enter** or click away
4. All references update:
   - Series using that column
   - X-axis selection
   - Labels in the graph

### Exporting Your Data

1. Click **"Export CSV"** button
2. Choose where to save the file
3. Your edited data is exported
4. Import it later or use in other tools

---

## 🔥 Real-Time Features

Every data change triggers:
1. **Automatic Type Detection**: Numbers converted to int/float, text kept as string
2. **Immediate Graph Update**: No refresh button needed
3. **Undo/Redo Support**: Ctrl+Z to undo, Ctrl+Y to redo
4. **State Preservation**: All edits saved in history

---

## 💡 Use Cases

### 1. Quick Data Adjustments
```
Scenario: You imported data but one value is wrong
Solution: Click the cell → Type correct value → Done!
```

### 2. Building Data from Scratch
```
Scenario: Start with blank data
Steps:
1. Load "New Blank Graph"
2. Add rows and columns
3. Enter your data
4. Add series
5. Customize and export
```

### 3. Experimenting with Values
```
Scenario: Testing "what-if" scenarios
Process:
1. Edit values to see impact
2. Watch graph change in real-time
3. Undo if needed (Ctrl+Z)
4. Try different values
```

### 4. Data Cleanup
```
Scenario: Remove outliers or bad data
Steps:
1. Identify problematic rows/columns
2. Delete or edit them
3. See cleaned graph immediately
```

---

## 📊 Integration with Series

The Data Editor integrates seamlessly with series controls:

### After Adding a Column:
1. New column appears in "Series" section's "Add Series" dropdown
2. Add it as a new series
3. Customize color, markers, style
4. See it plotted on the graph

### After Renaming a Column:
1. Series automatically updates to use new name
2. Legend shows new name
3. No need to reconfigure

### After Deleting a Column:
1. Series using that column are removed
2. Graph adjusts automatically
3. Clean state maintained

---

## ⚡ Performance

- **Display Limit**: Shows up to 10 rows × 6 columns for smooth performance
- **Full Data**: All data rows/columns still exist, just not all visible
- **Scrollable**: Scroll within the table to see more data
- **Efficient Updates**: Only affected parts re-render

---

## 🎨 UI Layout

```
Data Editor Section:
┌─────────────────────────────────────┐
│ [Add Row] [Delete Row] [Add Column] │
│ [Export CSV]                         │
├─────────────────────────────────────┤
│ Showing 10 of X rows, 6 of Y columns│
├───┬────────┬────────┬────────┬──────┤
│Row│ Col1   │ Col2   │ Col3   │ 🗑️  │ ← Headers (editable)
├───┼────────┼────────┼────────┼──────┤
│ 0 │  100   │  5.2   │  text  │      │ ← Data cells (editable)
│ 1 │  150   │  6.1   │  more  │      │
│ 2 │  200   │  4.8   │  data  │      │
└───┴────────┴────────┴────────┴──────┘
        ↑ Click any cell to edit
```

---

## 🎓 Tips & Tricks

1. **Quick Column Rename**: Double-click column header → type → Enter

2. **Batch Editing**: 
   - Edit multiple cells
   - Each change updates graph
   - Use Ctrl+Z to undo all at once

3. **Testing Values**:
   - Try different numbers
   - See instant visual feedback
   - Undo to revert

4. **Data Validation**:
   - App auto-converts numbers
   - Invalid numbers kept as text
   - Empty cells become null

5. **Column Management**:
   - Delete unused columns to declutter
   - Rename for better clarity
   - Add columns for calculated values

---

## 🚀 Advanced Workflows

### Workflow 1: Import → Edit → Export
```
1. Import CSV data
2. Fix any errors in Data Editor
3. Add calculated columns
4. Export cleaned data
```

### Workflow 2: Manual Data Entry
```
1. Start with blank graph
2. Add columns for your variables
3. Rename columns appropriately
4. Add rows with your data
5. Configure series and visualize
```

### Workflow 3: Interactive Analysis
```
1. Load your data
2. Edit values to test scenarios
3. Watch graph change in real-time
4. Find optimal parameters
5. Export final configuration
```

---

## ✅ What You Can Do

- ✅ Edit any cell value
- ✅ Add unlimited rows
- ✅ Add unlimited columns
- ✅ Delete rows and columns
- ✅ Rename columns
- ✅ Export edited data
- ✅ See all changes in real-time
- ✅ Undo/redo all changes
- ✅ Automatic type conversion
- ✅ Smart column name handling
- ✅ Series auto-update on column changes

---

## 🎉 Summary

The **Data Editor** gives you **complete control** over your data:

- **Full editing capabilities** - Change any value, any time
- **Structure management** - Add/remove/rename rows and columns
- **Real-time visualization** - Every change updates the graph instantly
- **Export functionality** - Save your edited data
- **Seamless integration** - Works perfectly with all series controls

**You now have a complete spreadsheet-like editor built right into your graph creator!** 📊✨

---

## Need More?

All data editing features work alongside:
- Series customization (colors, markers, styles)
- Axis controls (labels, scales, ranges)
- Annotations and themes
- All chart types
- Import/Export functionality

**Everything updates in real-time!**

