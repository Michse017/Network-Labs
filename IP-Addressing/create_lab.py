"""
Lab Structure Creator for Network Labs
---------------------------------------
Automatically generates standardized lab directory structure with templates.

Author: Network Labs
Version: 1.0
"""

import os
from pathlib import Path
from datetime import datetime


class LabStructureCreator:
    """
    Creates standardized directory structure for network laboratory exercises.
    """
    
    def __init__(self):
        """Initialize lab structure creator with project paths."""
        # Get project root directory
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.labs_dir = self.project_root / "labs"
        
    def create_lab_structure(self, lab_name: str, lab_description: str = ""):
        """
        Create complete laboratory directory structure.
        
        Args:
            lab_name (str): Laboratory name (e.g., lab01-vlans)
            lab_description (str): Brief description of the lab
            
        Returns:
            Path: Path to created lab directory, or None if cancelled
        """
        # Normalize lab name
        lab_name = lab_name.lower().strip()
        if not lab_name.startswith('lab'):
            lab_name = f"lab-{lab_name}"
        
        lab_path = self.labs_dir / lab_name
        
        # Check if lab already exists
        if lab_path.exists():
            overwrite = input(f"WARNING: Laboratory '{lab_name}' already exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                print("Operation cancelled.")
                return None
        
        print(f"\nCreating structure for: {lab_name}")
        print("=" * 70)
        
        # Create directory structure
        folders = [
            lab_path,
            lab_path / "configs" / "final",
            lab_path / "configs" / "step-by-step",
            lab_path / "verification",
            lab_path / "IP-Tables"
        ]
        
        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"Created: {folder.relative_to(self.project_root)}")
        
        # Create files
        self._create_readme(lab_path, lab_name, lab_description)
        self._create_gitkeep_files(lab_path)
        self._create_verification_templates(lab_path)
        self._create_topology_placeholder(lab_path)
        self._create_ip_tables_readme(lab_path)
        
        print("\n" + "=" * 70)
        print(f"Laboratory structure '{lab_name}' created successfully")
        print(f"Location: {lab_path.relative_to(self.project_root)}")
        print("\nNext steps:")
        print(f"  1. Edit README.md: {lab_path / 'README.md'}")
        print(f"  2. Add topology (.pkt): {lab_path}")
        print(f"  3. Capture topology screenshot (topology.png): {lab_path}")
        print(f"  4. Run vlsm_calculator.py with lab name: {lab_name}")
        print(f"  5. Document configurations: {lab_path / 'configs'}")
        
        return lab_path
    
    def _create_readme(self, lab_path: Path, lab_name: str, description: str):
        """
        Create README.md file with professional template.
        
        Args:
            lab_path (Path): Path to lab directory
            lab_name (str): Name of the laboratory
            description (str): Lab description
        """
        readme_path = lab_path / "README.md"
        
        # Extract lab number and topic
        parts = lab_name.split('-')
        lab_number = parts[0].replace('lab', '').zfill(2) if len(parts) > 0 else "XX"
        lab_topic = ' '.join(parts[1:]).title() if len(parts) > 1 else "Lab Topic"
        
        readme_content = f"""# Lab {lab_number} - {lab_topic}

## Objectives

- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3
- [ ] Verify connectivity
- [ ] Document configuration

## Network Topology

![Lab {lab_number} Topology](topology.png)

## IP Addressing Table

See [vlsm_table.md](IP-Tables/vlsm_table.md)

| Device | Interface | IP Address | Subnet Mask | VLAN/Network |
|--------|-----------|------------|-------------|--------------|
| R1     | G0/0      | X.X.X.X    | X.X.X.X     | -            |
| SW1    | VLAN1     | X.X.X.X    | X.X.X.X     | -            |
| PC1    | NIC       | X.X.X.X    | X.X.X.X     | -            |

## Network Design

{description if description else "Network design description..."}

## Configuration Steps

### 1. Basic Configuration

```cisco
# See complete commands in: configs/step-by-step/
enable
configure terminal
hostname DEVICE_NAME
```

### 2. Interface Configuration

```cisco
# Add specific interface configuration here
```

### 3. Protocol Configuration

```cisco
# Add protocol configuration (OSPF, EIGRP, etc.)
```

## Verification

### Verification Commands
See [show-commands.txt](verification/show-commands.txt)

### Connectivity Tests
See [ping-tests.txt](verification/ping-tests.txt)

## Lessons Learned

- Lesson 1
- Lesson 2
- Lesson 3

## Additional Resources

- [Cisco Documentation](https://www.cisco.com/)
- [Additional resource]

## Lab Information

- **Author**: Your Name
- **Date**: {self._get_current_date()}
- **Estimated Time**: XX minutes
- **Difficulty**: Intermediate
- **Technologies**: {lab_topic}

## Success Criteria

- [ ] Basic configuration completed
- [ ] Connectivity verified
- [ ] Protocols functioning correctly
- [ ] Configuration documented and backed up
"""
        
        readme_path.write_text(readme_content, encoding='utf-8')
        print(f"Created: {readme_path.relative_to(self.project_root)}")
    
    def _create_verification_templates(self, lab_path: Path):
        """
        Create verification template files.
        
        Args:
            lab_path (Path): Path to lab directory
        """
        # show-commands.txt template
        show_commands_content = """!==============================================================================
! VERIFICATION COMMANDS
!==============================================================================

!===== Router Commands =====
show ip interface brief
show ip route
show running-config
show ip protocols

!===== Switch Commands =====
show vlan brief
show interfaces trunk
show mac address-table
show spanning-tree
show running-config

!===== Additional Lab-Specific Commands =====
! Add specific commands here

!===== Expected Outputs =====
! Describe what should be observed in each command output
"""
        
        # ping-tests.txt template
        ping_tests_content = """!==============================================================================
! CONNECTIVITY TESTS
!==============================================================================

! Test 1: Local connectivity
! Device: PC1
! Target: PC2
! Expected: Success
PC> ping X.X.X.X

! Test 2: Inter-network connectivity
! Device: PC1
! Target: PC3 (different network)
! Expected: Success
PC> ping X.X.X.X

! Test 3: Gateway verification
! Device: PC1
! Target: Default Gateway
! Expected: Success
PC> ping X.X.X.X

!===== Traceroute Tests =====
! Verify packet path
PC> tracert X.X.X.X

!===== Expected Results =====
! All pings should succeed
! Latency should be less than Xms
! 0% packet loss
"""
        
        verification_dir = lab_path / "verification"
        (verification_dir / "show-commands.txt").write_text(show_commands_content, encoding='utf-8')
        (verification_dir / "ping-tests.txt").write_text(ping_tests_content, encoding='utf-8')
        
        print(f"Created verification templates")
    
    def _create_gitkeep_files(self, lab_path: Path):
        """
        Create .gitkeep files to preserve empty directories in git.
        
        Args:
            lab_path (Path): Path to lab directory
        """
        gitkeep_paths = [
            lab_path / "configs" / "final" / ".gitkeep",
            lab_path / "configs" / "step-by-step" / ".gitkeep",
        ]
        
        for gitkeep in gitkeep_paths:
            gitkeep.write_text("", encoding='utf-8')
    
    def _create_ip_tables_readme(self, lab_path: Path):
        """
        Create README file in IP-Tables directory.
        
        Args:
            lab_path (Path): Path to lab directory
        """
        ip_tables_readme = lab_path / "IP-Tables" / "README.md"
        content = """# IP Addressing Tables

This directory contains the IP addressing plan for this laboratory.

## Files

- `vlsm_table.md` - IP addressing table in Markdown format
- `vlsm_table.csv` - IP addressing table in CSV format

## Generation

These files are automatically generated using:

```bash
python IP-Addressing/vlsm_calculator.py
```

Enter the lab name when prompted to save tables to this directory.
"""
        ip_tables_readme.write_text(content, encoding='utf-8')
        print(f"Created IP-Tables README")
    
    def _create_topology_placeholder(self, lab_path: Path):
        """
        Create instruction file for topology completion.
        
        Args:
            lab_path (Path): Path to lab directory
        """
        instructions_path = lab_path / "TOPOLOGY-INSTRUCTIONS.txt"
        content = """LAB COMPLETION INSTRUCTIONS
==============================================================================

1. TOPOLOGY:
   - Create topology in Cisco Packet Tracer
   - Save file as: topology.pkt or [lab-name].pkt
   - Take screenshot and save as: topology.png

2. IP ADDRESSING:
   - Execute: python IP-Addressing/vlsm_calculator.py
   - Enter this lab name when prompted
   - Tables will be automatically saved to IP-Tables/

3. CONFIGURATIONS:
   - In configs/step-by-step/: Save configuration commands
   - In configs/final/: Save 'show running-config' output
   - Name files by device: R1-config.txt, SW1-final.txt

4. VERIFICATION:
   - Complete verification/show-commands.txt with actual outputs
   - Complete verification/ping-tests.txt with test results

5. DOCUMENTATION:
   - Update README.md with specific information
   - Add screenshots if necessary

This file can be deleted once these steps are completed.
"""
        instructions_path.write_text(content, encoding='utf-8')
        print(f"Created: TOPOLOGY-INSTRUCTIONS.txt")
    
    def _get_current_date(self):
        """
        Get current date in ISO format.
        
        Returns:
            str: Current date (YYYY-MM-DD)
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    def list_existing_labs(self):
        """List all existing laboratory directories."""
        if not self.labs_dir.exists():
            print("ERROR: 'labs' directory not found")
            return
        
        labs = sorted([d for d in self.labs_dir.iterdir() if d.is_dir()])
        
        if not labs:
            print("No laboratories created yet.")
            return
        
        print("\nExisting Laboratories:")
        print("=" * 70)
        for i, lab in enumerate(labs, 1):
            print(f"  {i}. {lab.name}")
        print("=" * 70)


def main():
    """Main execution function for interactive lab creation."""
    creator = LabStructureCreator()
    
    print("=" * 70)
    print("LAB STRUCTURE CREATOR")
    print("=" * 70)
    
    # Display existing labs
    creator.list_existing_labs()
    
    print("\nWhat would you like to do?")
    print("1. Create new laboratory")
    print("2. Exit")
    
    choice = input("\nSelect option (1-2): ").strip()
    
    if choice == "1":
        print("\n" + "=" * 70)
        lab_name = input("Laboratory name (e.g., lab01-vlans, ospf, acls): ").strip()
        
        if not lab_name:
            print("ERROR: Laboratory name is required")
            return
        
        description = input("Brief description (optional, press Enter to skip): ").strip()
        
        creator.create_lab_structure(lab_name, description)
    else:
        print("Exiting...")


if __name__ == "__main__":
    main()