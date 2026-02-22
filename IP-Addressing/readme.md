# IP Addressing Tools

Professional tools for subnet calculation and VLSM (Variable Length Subnet Masking) designed for network laboratory exercises.

## Available Tools

### 1. VLSM Calculator (`vlsm_calculator.py`)
Automatically calculates VLSM subnets based on host requirements and generates comprehensive IP addressing tables.

**Features:**
- Automatic subnet calculation based on host count
- Optimal subnet allocation (largest to smallest)
- Exports to Markdown and CSV formats
- Integration with lab directory structure

### 2. Lab Structure Creator (`create_lab.py`)
Generates standardized laboratory directory structure with professional templates.

**Features:**
- Creates complete lab directory structure
- Generates README templates
- Creates verification command templates
- Includes gitkeep files for version control

## Quick Start

### Create New Lab
```bash
python IP-Addressing/create_lab.py
```

### Generate VLSM Tables for Lab
```bash
python IP-Addressing/vlsm_calculator.py
```

## Workflow Example

1. **Create lab structure:**
   ```bash
   python IP-Addressing/create_lab.py
   # Enter: vlans
   ```

2. **Generate IP addressing plan:**
   ```bash
   python IP-Addressing/vlsm_calculator.py
   # Enter lab name: vlans
   # Enter base network: 192.168.1.0/24
   # Define subnet requirements
   ```

3. **Output location:**
   ```
   labs/lab-vlans/IP-Tables/
   ├── vlsm_table.md
   └── vlsm_table.csv
   ```

## Output Files

### Markdown Table (`vlsm_table.md`)
Human-readable IP addressing table suitable for documentation and README files.

### CSV Table (`vlsm_table.csv`)
Machine-readable format for spreadsheet applications and automated processing.

## Integration

Both tools are designed to work together:
- Use the **same lab name** in both scripts
- Lab structure creator prepares the directory
- VLSM calculator populates IP-Tables directory automatically

## Requirements

- Python 3.7+
- No external dependencies (uses standard library only)

## Notes

- Lab names are automatically normalized (lowercase, 'lab-' prefix)
- IP-Tables directory is created automatically if missing
- Both tools support fallback to `IP-Addressing/tables/` if lab directory not found