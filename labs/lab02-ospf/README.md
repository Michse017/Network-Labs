# Lab 02 – OSPF Routing

## Objectives

- Configure OSPF in a single area (Area 0) across multiple routers.
- Advertise networks using OSPF and verify neighbor adjacencies.
- Examine the OSPF link-state database (LSDB) and routing table.
- Optionally extend to a multi-area OSPF design.

## Prerequisites

- Cisco Packet Tracer 8.x or later.
- Completion of Lab 01 (VLANs & Trunking) is recommended.
- Basic understanding of IP routing and subnetting.

## Topology

```
        10.0.12.0/30          10.0.23.0/30
R1 ─────────────────── R2 ─────────────────── R3
 \                                             /
  \───────────── 10.0.13.0/30 ───────────────/
```

- **R1**, **R2**, and **R3** are Cisco ISR routers.
- All routers participate in **OSPF Area 0**.
- Loopback interfaces are used as Router IDs.

## IP Addressing

| Device | Interface     | IP Address      | Subnet Mask     | Description       |
|--------|---------------|-----------------|-----------------|-------------------|
| R1     | Loopback0     | 1.1.1.1         | 255.255.255.255 | Router ID         |
| R1     | Gi0/0         | 10.0.12.1       | 255.255.255.252 | Link to R2        |
| R1     | Gi0/1         | 10.0.13.1       | 255.255.255.252 | Link to R3        |
| R2     | Loopback0     | 2.2.2.2         | 255.255.255.255 | Router ID         |
| R2     | Gi0/0         | 10.0.12.2       | 255.255.255.252 | Link to R1        |
| R2     | Gi0/1         | 10.0.23.1       | 255.255.255.252 | Link to R3        |
| R3     | Loopback0     | 3.3.3.3         | 255.255.255.255 | Router ID         |
| R3     | Gi0/0         | 10.0.13.2       | 255.255.255.252 | Link to R1        |
| R3     | Gi0/1         | 10.0.23.2       | 255.255.255.252 | Link to R2        |

## Step-by-Step Instructions

### Step 1 – Configure Interfaces on R1

```
R1> enable
R1# configure terminal
R1(config)# interface Loopback0
R1(config-if)# ip address 1.1.1.1 255.255.255.255
R1(config-if)# exit
R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip address 10.0.12.1 255.255.255.252
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)# interface GigabitEthernet0/1
R1(config-if)# ip address 10.0.13.1 255.255.255.252
R1(config-if)# no shutdown
R1(config-if)# exit
```

### Step 2 – Enable OSPF on R1

```
R1(config)# router ospf 1
R1(config-router)# router-id 1.1.1.1
R1(config-router)# network 1.1.1.1 0.0.0.0 area 0
R1(config-router)# network 10.0.12.0 0.0.0.3 area 0
R1(config-router)# network 10.0.13.0 0.0.0.3 area 0
R1(config-router)# end
R1# write memory
```

### Step 3 – Repeat for R2 and R3

Configure interfaces and OSPF on R2 and R3 using the addressing table above.

## Verification

```
R1# show ip ospf neighbor
R1# show ip route ospf
R1# show ip ospf database
```

## Files

| File | Description |
|------|-------------|
| `topology.pkt` | Packet Tracer simulation file |
| `topology.png` | Topology diagram |
| `configs/` | Running configurations for R1, R2, R3 |
| `verifications/` | OSPF neighbor, route, and database outputs |
