---
title: "Firewall - VyOS"
date: 2024-09-24
lastmod: 2024-09-24
draft: false
description: "projekt firewall"
featureimage: "https://github.com/catalyys/catalyys.github.io/blob/main/assets/azubi_umgebung_setup.svg?raw=true"
tags: ["fisi", "übung", "projekt"]
type: "projekt"
series: ["Projekt"]
series_order: 2
showPagination: true
---

## Informationen

Bei der [Installation](https://docs.vyos.io/en/latest/installation/install.html#permanent-installation) könnt ihr euch an die Standards halten.

Mit dem Befehl `set system option keyboard-layout de`  könnt ihr die Tastatur auf Deutsch in der Installation umstellen.

Im [Quick Start Guide](https://docs.vyos.io/en/latest/quick-start.html) findet ihr viele Informationen, die bei dem Aufbau helfen werden.

Wichtig ist, `commit` und `save` auszuführen.

Hier nochmal das Bild mit dem Aufbau für die IP Adressen und DHCP Pools.
![Netz Aufbau](azubi_umgebung_setup.svg "Netz Aufbau")

## System

Zuerst folgen die allgemeinen Einstellungen die nach der [Installation](https://docs.vyos.io/en/latest/installation/install.html#permanent-installation) gemacht werden sollten.

### VM Einstellungen

Auch hier wird die VM in bestimmt Netze gepackt.

![internes Netz](azubi_projekt_fw_bridge.png "Einstellung in VirtualBox")

![internes Netz](azubi_projekt_fw_internal.png "Einstellung in VirtualBox")

Und der dritte Adapter auch **internal Network**, aber **test**.

#### Interfaces

Die Relation zu den Interfaces auf der Firewall ist dann folgende:
- eth0 -> Adapter1
- eth1 -> Adapter2
- eth2 -> Adapter3


### System Konfiguration

Wichtige Vorabeinstellungen im System.

```
set system option keyboard-layout de

set interfaces ethernet eth0 address dhcp

set service ssh port 22
set service ssh listen-address <erhaltene IP Adresse>
```


## DHCP

Hier muss der DHCP Server aktiviert werden für die beiden Netze, in denen sich die Linux VMs befinden.
Dazu könnt ihr den [Quick Start Guide](https://docs.vyos.io/en/latest/quick-start.html) nehmen oder die [DHCP Doku](https://docs.vyos.io/en/latest/configuration/service/dhcp-server.html)

Sobald alles funktioniert, sollten eure Linux VMs eine IP erhalten

{{< collapsible label="Lösung DHCP setup" >}}
```
set interfaces ethernet eth2 address 10.100.2.254/24
set service dhcp-server shared-network-name test subnet 10.100.2.0/24 option default-router 10.100.2.254
set service dhcp-server shared-network-name test subnet 10.100.2.0/24 range 0 start 10.100.2.10
set service dhcp-server shared-network-name test subnet 10.100.2.0/24 range 0 stop 10.100.2.100
set service dhcp-server shared-network-name test subnet 10.100.2.0/24 subnet-id '2'

set interfaces ethernet eth1 address 10.100.1.254/24
set service dhcp-server shared-network-name prod subnet 10.100.1.0/24 option default-router 10.100.1.254
set service dhcp-server shared-network-name prod subnet 10.100.1.0/24 range 0 start 10.100.1.10
set service dhcp-server shared-network-name prod subnet 10.100.1.0/24 range 0 stop 10.100.1.100
set service dhcp-server shared-network-name prod subnet 10.100.1.0/24 subnet-id '1'
```
{{< /collapsible >}}

## Firewall

Im nächsten Schritt wird die Firewall aktiviert. Dabei soll erstmal nur ICMP erlaubt werden zwischen den Netzen.
Aktiviert dabei auch 

Da VyOS auf Linux basiert, werden die Firewall Regeln über iptables/nftables gesteuert. Dabei werden Chains benutzt, um die Regeln zu gruppieren und zu unterteilen. Für die Übung reichen die Standard Chains die schon vorhanden sind. Die Input Chain ist für den Traffic, der für die Firewall bestimmt ist und die Forward Chain für den restlichen Traffic. Das heißt alle Regeln zwischen den Netzen muss in die Forward Chain.

Um einen genaueren Blick zu erhalten könnt ihr euch folgende Artikel durchlesen:
- [Quick Start Guide](https://docs.vyos.io/en/latest/quick-start.html#firewall)
- [Configuration Guide -> Firewall](https://docs.vyos.io/en/latest/configuration/firewall/)
- [Zone Based Firewall](https://docs.vyos.io/en/latest/configuration/firewall/zone.html)


{{< collapsible label="Lösung Firewall setup" >}}
```
# globale optionen
set firewall global-options state-policy established action accept
set firewall global-options state-policy related action accept
set firewall global-options state-policy invalid action drop

# default action drop und log aktivieren
set firewall ipv4 forward filter default-action drop
set firewall ipv4 forward filter default-log

# regel 100: accept icmp
set firewall ipv4 forward filter rule 100 action accept
set firewall ipv4 forward filter rule 100 protocol icmp
```
{{< /collapsible >}}

## NAT

Zuletzt braucht ihr Internet auf euren Linux VMs. Das stellt ihr mit **NAT** bereit.

Dazu hilt die Doku zu [NAT](https://docs.vyos.io/en/latest/configuration/nat/nat44.html) und mal wieder der [Quick Start Guide](https://docs.vyos.io/en/latest/quick-start.html).

{{< collapsible label="Lösung NAT setup" >}}
```
set nat source rule 100 outbound-interface name eth0
set nat source rule 100 source address 10.100.1.0/24
set nat source rule 100 translation address masquerade

set nat source rule 110 outbound-interface name eth0
set nat source rule 110 source address 10.100.2.0/24
set nat source rule 110 translation address masquerade
```
{{< /collapsible >}}





