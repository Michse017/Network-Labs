# Scripts

This directory contains automation and utility scripts for the lab environment.

## Structure

```
scripts/
├─ README.md
├─ backup-configs.sh      # Collect running configs from devices via SSH
└─ verify-connectivity.py # Ping sweep to verify end-to-end connectivity
```

## Usage

### backup-configs.sh

Connects to each device via SSH and saves the running configuration locally.

```bash
chmod +x backup-configs.sh
./backup-configs.sh
```

### verify-connectivity.py

Performs a ping sweep across defined subnets and reports reachability.

```bash
pip install netmiko
python verify-connectivity.py
```

## Requirements

- Python 3.8+
- [Netmiko](https://github.com/ktbyers/netmiko) for SSH-based device interaction
- SSH access enabled on all target devices
