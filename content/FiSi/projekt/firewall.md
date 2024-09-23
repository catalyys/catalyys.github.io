---
title: "Firewall - VyOS"
date: 2024-09-22
lastmod: 2024-09-22
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


set interfaces ethernet eth1 address 10.100.1.254/24
set service dhcp-server shared-network-name prod subnet 10.100.1.0/24 option default-router 10.100.1.254
set service dhcp-server shared-network-name prod subnet 10.100.1.0/24 range 0 start 10.100.1.10
set service dhcp-server shared-network-name prod subnet 10.100.1.0/24 range 0 stop 10.100.1.100
```
{{< /collapsible >}}

## Firewall

Im nächsten Schritt wird die Firewall aktiviert. Dabei soll erstmal nur ICMP erlaubt werden zwischen den Netzen.

Hierbei schaut ihr euch die Doku zur [Zone Based Firewall](https://docs.vyos.io/en/latest/configuration/firewall/zone.html) durch und wieder den Abschnitt im [Quick Start Guide](https://docs.vyos.io/en/latest/quick-start.html).

{{< alert >}}
Damit das nicht zu Kompliziert wird, könnt ihr nur eine Chain nehmen und in dieser alle Regeln verwalten.
{{< /alert >}}

{{< collapsible label="Lösung Firewall setup" >}}
```
set firewall global-options state-policy established action accept
set firewall global-options state-policy related action accept
set firewall global-options state-policy invalid action drop

set firewall ipv4 name test-prod default-action drop
set firewall ipv4 name test-prod default-log



set firewall ipv4 name test-prod rule 100 action accept
set firewall ipv4 name test-prod rule 100 protocol icmp

set firewall zone prod from test firewall name test-prod
set firewall zone test from prod firewall name test-prod



set firewall zone test default-action drop
set firewall zone test interface eth2

set firewall zone prod default-action drop
set firewall zone prod interface eth1
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

## Quick Start

ToDo: Ansible playbook schreiben



