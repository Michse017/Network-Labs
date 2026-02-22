# Diagrams

This directory contains clean, presentation-ready network diagrams.

## Supported Formats

| Format | Extension | Tool |
|--------|-----------|------|
| draw.io | `.xml` | [draw.io](https://draw.io) / [diagrams.net](https://diagrams.net) |
| Scalable Vector Graphics | `.svg` | Any vector editor or draw.io |
| Portable Network Graphics | `.png` | Exported from draw.io or Packet Tracer |

## File Naming Convention

```
<lab-id>-<description>.<ext>
```

Examples:
- `lab01-vlans-topology.xml`
- `lab02-ospf-topology.svg`
- `network-overview.png`

## How to Add a Diagram

1. Create or export your diagram from draw.io (File → Export As → XML or SVG).
2. Place the file in this directory following the naming convention above.
3. Reference it from the relevant lab `README.md`.
