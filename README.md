# Network-Labs

A comprehensive networking lab repository covering core networking concepts, switching and routing technologies, troubleshooting methodologies, and network automation practices. Labs include documented topologies, device configurations, verification outputs, and structured analysis for continuous learning and skill development.

## Repository Structure

```
network-labs/
├─ README.md                     # General index and purpose
├─ LICENSE
├─ .gitignore
├─ labs/
│  ├─ lab01-vlans/               # Each lab in its own folder
│  │  ├─ README.md               # Objectives, steps, verification
│  │  ├─ topology.pkt            # Packet Tracer file
│  │  ├─ topology.png            # Exported topology image
│  │  ├─ configs/
│  │  │  ├─ sw1-running-config.txt
│  │  │  └─ r1-running-config.txt
│  │  ├─ verifications/
│  │  │  ├─ show_vlan.txt
│  │  │  └─ show_interfaces_trunk.txt
│  │  └─ captures/               # Optional pcap or logs
│  └─ lab02-ospf/
├─ diagrams/                     # Clean diagrams (draw.io .xml / svg)
└─ scripts/                      # Automation scripts if applicable
```

## How to Use

1. Navigate to the desired lab folder under `labs/`.
2. Read the lab's `README.md` for objectives, prerequisites, and step-by-step instructions.
3. Open `topology.pkt` in Cisco Packet Tracer to load the network topology.
4. Follow the configuration steps and verify using the outputs in the `verifications/` folder.
5. Compare your device configs with the samples in `configs/`.
