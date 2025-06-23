---
title: "DHCP"
date: 2024-09-02
lastmod: 2024-09-10
draft: true
description: "dhcp mit IPv4"
tags: ["fisi", "dhcp", "übung"]
type: "übung"
---

## Anleitung

### *dhcp* konfigurieren allgemein

wichtige Dateien:
- `/etc/dhcp/dhcpd.conf`
- `/etc/dhcp/dhcpd6.conf`
- `/etc/default/isc-dhcp-server`

Unter `dhcpd.conf` werden die IPv4 Subnetze konfiguriert und in `dhcpd6.conf` die IPv6 Subnetze.
In `isc-dhcp-server` werden die Listen Interfaces konfiguriert und extra Argumente können dem Dienst übergeben werden.

#### Beispiele

```bash
subnet 192.168.1.0 netmask 255.255.255.0 {
        option routers                  192.168.1.254;
        option subnet-mask              255.255.255.0;
        option domain-search            "example.com";
        option domain-name-servers      192.168.1.1;
		range 192.168.1.10 192.168.1.100;
}
```

```bash
subnet6 2001:db8:0:1::/64 {
        range6 2001:db8:0:1::129 2001:db8:0:1::254;
        option dhcp6.name-servers fec0:0:0:1::1;
        option dhcp6.domain-search "domain.example";
}
```

#### Troubleshooting

Zum Troubleshooting könnt ihr folgendes versuchen:
- `journalctl -eu dhcpd.service` für logs

---

