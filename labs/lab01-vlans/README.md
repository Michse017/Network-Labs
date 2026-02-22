# Lab 01 – VLANs & Trunking

## Objectives

- Create and name VLANs on Cisco switches.
- Assign access ports to the appropriate VLANs.
- Configure trunk links between switches.
- Verify VLAN membership and trunk status.

## Prerequisites

- Cisco Packet Tracer 8.x or later.
- Basic knowledge of the Cisco IOS CLI.

## Topology

```
PC1 (VLAN 10) ──── SW1 ════ SW2 ──── PC3 (VLAN 10)
PC2 (VLAN 20) ──┘            └───── PC4 (VLAN 20)
```

- **SW1** and **SW2** are Cisco 2960 switches.
- The link between SW1 and SW2 is a **802.1Q trunk**.
- PCs use static IP addressing within their VLAN subnets.

## IP Addressing

| Device | Interface | VLAN | IP Address    | Subnet Mask   |
|--------|-----------|------|---------------|---------------|
| PC1    | Fa0       | 10   | 192.168.10.1  | 255.255.255.0 |
| PC2    | Fa0       | 20   | 192.168.20.1  | 255.255.255.0 |
| PC3    | Fa0       | 10   | 192.168.10.2  | 255.255.255.0 |
| PC4    | Fa0       | 20   | 192.168.20.2  | 255.255.255.0 |

## Step-by-Step Instructions

### Step 1 – Create VLANs on SW1

```
SW1> enable
SW1# configure terminal
SW1(config)# vlan 10
SW1(config-vlan)# name SALES
SW1(config-vlan)# exit
SW1(config)# vlan 20
SW1(config-vlan)# name ENGINEERING
SW1(config-vlan)# exit
```

### Step 2 – Assign Access Ports on SW1

```
SW1(config)# interface FastEthernet0/1
SW1(config-if)# switchport mode access
SW1(config-if)# switchport access vlan 10
SW1(config-if)# exit
SW1(config)# interface FastEthernet0/2
SW1(config-if)# switchport mode access
SW1(config-if)# switchport access vlan 20
SW1(config-if)# exit
```

### Step 3 – Configure the Trunk Port on SW1

```
SW1(config)# interface GigabitEthernet0/1
SW1(config-if)# switchport mode trunk
SW1(config-if)# switchport trunk allowed vlan 10,20
SW1(config-if)# exit
SW1(config)# end
SW1# write memory
```

### Step 4 – Repeat on SW2

Repeat Steps 1–3 on SW2, assigning PC3 to VLAN 10 and PC4 to VLAN 20.

## Verification

After completing the configuration, use the following commands and compare the output with the files in the `verifications/` folder:

```
SW1# show vlan brief
SW1# show interfaces trunk
```

See [`verifications/show_vlan.txt`](verifications/show_vlan.txt) and [`verifications/show_interfaces_trunk.txt`](verifications/show_interfaces_trunk.txt).

## Troubleshooting Tips

- If a port does not appear in `show vlan brief`, verify it is set to `switchport mode access`.
- If the trunk is not established, confirm both ends are set to `switchport mode trunk` or use `switchport mode dynamic desirable`.
- Ensure the allowed VLAN list on the trunk includes the VLANs you created.

## Files

| File | Description |
|------|-------------|
| `topology.pkt` | Packet Tracer simulation file |
| `topology.png` | Topology diagram |
| `configs/sw1-running-config.txt` | SW1 running configuration |
| `configs/r1-running-config.txt` | R1 running configuration (for inter-VLAN routing) |
| `verifications/show_vlan.txt` | Output of `show vlan brief` |
| `verifications/show_interfaces_trunk.txt` | Output of `show interfaces trunk` |
