"""
VLSM Calculator for Network Labs
---------------------------------
Calculates Variable Length Subnet Masks (VLSM) based on host requirements.
Automatically saves IP addressing tables to the corresponding lab directory.

Author: Network Labs
Version: 1.0
"""

import ipaddress
from typing import List, Tuple
from pathlib import Path


class VLSMCalculator:
    """
    VLSM Calculator class for automatic subnet calculation and documentation.
    """
    
    def __init__(self, network: str, lab_name: str = None):
        """
        Initialize VLSM calculator with base network.
        
        Args:
            network (str): Base network in CIDR notation (e.g., "192.168.1.0/24")
            lab_name (str, optional): Associated lab name for output directory
        """
        self.base_network = ipaddress.IPv4Network(network, strict=False)
        self.subnets = []
        
        # Determine project root and output directory
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        
        if lab_name:
            # Normalize lab name to lowercase
            lab_name = lab_name.lower().strip()
            if not lab_name.startswith('lab'):
                lab_name = f"lab-{lab_name}"
            
            # Build path to existing lab directory
            lab_dir = self.project_root / "labs" / lab_name
            
            # Check if lab exists
            if not lab_dir.exists():
                print(f"WARNING: Lab directory '{lab_name}' does not exist")
                print(f"Please create it first using: python IP-Addressing/create_lab.py")
                print(f"Falling back to IP-Addressing/tables/")
                self.output_dir = self.script_dir / "tables"
            else:
                # Use existing IP-Tables directory
                self.output_dir = lab_dir / "IP-Tables"
                
                # Verify IP-Tables directory exists
                if not self.output_dir.exists():
                    print(f"WARNING: IP-Tables directory not found in {lab_name}")
                    print(f"Creating IP-Tables directory...")
                    self.output_dir.mkdir(parents=True, exist_ok=True)
        else:
            # Fallback to IP-Addressing/tables/
            self.output_dir = self.script_dir / "tables"
        
        # Create output directory if it doesn't exist (for fallback case)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.lab_name = lab_name
    
    def calculate_subnet_size(self, hosts_needed: int) -> int:
        """
        Calculate required subnet size for given number of hosts.
        
        Args:
            hosts_needed (int): Number of hosts required
            
        Returns:
            int: Subnet prefix length (CIDR notation)
        """
        # Add 2 for network and broadcast addresses
        total_addresses = hosts_needed + 2
        
        # Find next power of 2
        bits_needed = 0
        while 2 ** bits_needed < total_addresses:
            bits_needed += 1
        
        # Calculate new prefix length
        new_prefix = 32 - bits_needed
        return new_prefix
    
    def create_vlsm_subnets(self, host_requirements: List[Tuple[str, int]]):
        """
        Create VLSM subnets based on host requirements.
        
        Args:
            host_requirements (List[Tuple[str, int]]): List of (subnet_name, host_count)
        """
        # Sort by host count (descending order for optimal VLSM)
        sorted_requirements = sorted(host_requirements, key=lambda x: x[1], reverse=True)
        
        available_network = self.base_network
        self.subnets = []
        
        # Display header
        print("\n" + "=" * 80)
        if self.lab_name:
            print(f"VLSM Calculator - Lab: {self.lab_name}")
        print(f"Base Network: {self.base_network}")
        print("=" * 80 + "\n")
        
        # Process each subnet requirement
        for name, hosts in sorted_requirements:
            prefix_length = self.calculate_subnet_size(hosts)
            
            # Validate prefix length
            if prefix_length < available_network.prefixlen:
                print(f"ERROR: Insufficient space for subnet '{name}'")
                print(f"       Required: /{prefix_length}, Available: /{available_network.prefixlen}")
                continue
            
            # Create subnet
            subnet = ipaddress.IPv4Network(
                f"{available_network.network_address}/{prefix_length}", 
                strict=False
            )
            
            # Calculate subnet information
            usable_hosts = subnet.num_addresses - 2
            network_address = subnet.network_address
            broadcast_address = subnet.broadcast_address
            first_usable = network_address + 1
            last_usable = broadcast_address - 1
            subnet_mask = subnet.netmask
            wildcard_mask = subnet.hostmask
            
            # Store subnet information
            subnet_info = {
                'name': name,
                'hosts_required': hosts,
                'subnet': str(subnet),
                'network': str(network_address),
                'broadcast': str(broadcast_address),
                'first_usable': str(first_usable),
                'last_usable': str(last_usable),
                'usable_hosts': usable_hosts,
                'subnet_mask': str(subnet_mask),
                'wildcard_mask': str(wildcard_mask),
                'prefix': f"/{prefix_length}"
            }
            
            self.subnets.append(subnet_info)
            self.print_subnet_info(subnet_info)
            
            # Move to next available network block
            next_network = int(broadcast_address) + 1
            available_network = ipaddress.IPv4Network(
                f"{ipaddress.IPv4Address(next_network)}/{available_network.prefixlen}", 
                strict=False
            )
    
    def print_subnet_info(self, info: dict):
        """
        Print subnet information in readable format.
        
        Args:
            info (dict): Dictionary containing subnet information
        """
        print(f"Subnet: {info['name']}")
        print(f"  Hosts Required:     {info['hosts_required']}")
        print(f"  Network:            {info['subnet']}")
        print(f"  Network Address:    {info['network']}")
        print(f"  Subnet Mask:        {info['subnet_mask']}")
        print(f"  Wildcard Mask:      {info['wildcard_mask']}")
        print(f"  First Usable IP:    {info['first_usable']}")
        print(f"  Last Usable IP:     {info['last_usable']}")
        print(f"  Broadcast Address:  {info['broadcast']}")
        print(f"  Total Usable Hosts: {info['usable_hosts']}")
        print()
    
    def export_to_markdown(self, filename: str = "vlsm_table.md"):
        """
        Export subnets to Markdown table format.
        
        Args:
            filename (str): Output filename
        """
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# VLSM IP Addressing Plan\n\n")
            
            if self.lab_name:
                f.write(f"**Laboratory:** {self.lab_name}\n")
            
            f.write(f"**Base Network:** {self.base_network}\n\n")
            
            # Table header
            f.write("| Subnet | Hosts Req. | Network/Prefix | First IP | Last IP | Broadcast | Subnet Mask | Available Hosts |\n")
            f.write("|--------|------------|----------------|----------|---------|-----------|-------------|----------------|\n")
            
            # Table rows
            for subnet in self.subnets:
                f.write(f"| {subnet['name']} | {subnet['hosts_required']} | "
                       f"{subnet['subnet']} | {subnet['first_usable']} | "
                       f"{subnet['last_usable']} | {subnet['broadcast']} | "
                       f"{subnet['subnet_mask']} | {subnet['usable_hosts']} |\n")
        
        print(f"SUCCESS: Markdown table exported to {filepath}\n")
    
    def export_to_csv(self, filename: str = "vlsm_table.csv"):
        """
        Export subnets to CSV format.
        
        Args:
            filename (str): Output filename
        """
        import csv
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'Subnet', 'Hosts Required', 'Network/Prefix', 'Network Address',
                'Subnet Mask', 'First IP', 'Last IP', 'Broadcast', 'Available Hosts'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for subnet in self.subnets:
                writer.writerow({
                    'Subnet': subnet['name'],
                    'Hosts Required': subnet['hosts_required'],
                    'Network/Prefix': subnet['subnet'],
                    'Network Address': subnet['network'],
                    'Subnet Mask': subnet['subnet_mask'],
                    'First IP': subnet['first_usable'],
                    'Last IP': subnet['last_usable'],
                    'Broadcast': subnet['broadcast'],
                    'Available Hosts': subnet['usable_hosts']
                })
        
        print(f"SUCCESS: CSV table exported to {filepath}\n")


def main():
    """
    Main execution function for interactive VLSM calculation.
    """
    print("VLSM Calculator - Network Labs")
    print("=" * 80 + "\n")
    
    # Get lab name
    lab_name = input("Enter lab name (e.g., lab01-vlans) or press Enter to skip: ").strip()
    if not lab_name:
        lab_name = None
    
    # Get base network
    network = input("Enter base network (e.g., 192.168.1.0/24): ").strip()
    if not network:
        network = "192.168.1.0/24"
    
    # Create calculator instance
    calc = VLSMCalculator(network, lab_name)
    
    # Get input method preference
    print("\nHow would you like to input subnet requirements?")
    print("1. Manual input (one by one)")
    print("2. Use predefined example")
    choice = input("Select option (1 or 2): ").strip()
    
    subnets_data = []
    
    if choice == "1":
        # Manual input
        print("\nEnter subnet requirements (type 'done' when finished):\n")
        while True:
            name = input("Subnet name (or 'done' to finish): ").strip()
            if name.lower() == 'done':
                break
            
            try:
                hosts = int(input(f"Number of hosts for {name}: ").strip())
                subnets_data.append((name, hosts))
            except ValueError:
                print("ERROR: Please enter a valid number")
    else:
        # Predefined example
        subnets_data = [
            ("Sales", 50),
            ("IT", 25),
            ("Management", 10),
            ("P2P-Router1-Router2", 2),
            ("P2P-Router2-Router3", 2)
        ]
        print("\nUsing predefined example subnets")
    
    # Calculate VLSM
    calc.create_vlsm_subnets(subnets_data)
    
    # Export results
    calc.export_to_markdown()
    calc.export_to_csv()
    
    print("=" * 80)
    print("VLSM calculation completed successfully")
    
    if lab_name:
        print(f"Output saved to: labs/{lab_name}/IP-Tables/")
    
    print("=" * 80)


if __name__ == "__main__":
    main()