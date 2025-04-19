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
```


## DHCP

Hier muss der DHCP Server aktiviert werden für die beiden Netze, in denen sich die Linux VMs befinden.
Dazu könnt ihr den [Quick Start Guide](https://docs.vyos.io/en/latest/quick-start.html) nehmen oder die [DHCP Doku](https://docs.vyos.io/en/latest/configuration/service/dhcp-server.html)

Sobald alles funktioniert, sollten eure Linux VMs eine IP erhalten

{{< collapsible label="Lösung DHCP setup" >}}

{{< code language="vyos" source="/vagrant/configs/vyos/vyos.cfg" id="dhcp">}}

{{< /collapsible >}}

## Firewall

Im nächsten Schritt wird die Firewall aktiviert. Dabei soll erstmal nur ICMP erlaubt werden zwischen den Netzen.
Aktiviert dabei auch 

Da VyOS auf Linux basiert, werden die Firewall Regeln über iptables/nftables gesteuert. Dabei werden Chains benutzt, um die Regeln zu gruppieren und zu unterteilen. Für die Übung reichen die Standard Chains die schon vorhanden sind. Die **Input** Chain ist für den Traffic, der für die Firewall bestimmt ist und die Forward Chain für den restlichen Traffic. Das heißt alle Regeln zwischen den Netzen muss in die **Forward** Chain.

![VyOS Chains vereinfacht](firewall_chains.svg)

Um einen genaueren Blick zu erhalten könnt ihr euch folgende Artikel durchlesen:
- [Quick Start Guide](https://docs.vyos.io/en/latest/quick-start.html#firewall)
- [Configuration Guide -> Firewall](https://docs.vyos.io/en/latest/configuration/firewall/)
- [Zone Based Firewall](https://docs.vyos.io/en/latest/configuration/firewall/zone.html)


{{< collapsible label="Lösung Firewall setup" >}}

{{< code language="vyos" source="/vagrant/configs/vyos/vyos.cfg" id="firewall">}}

{{< /collapsible >}}

## NAT

Zuletzt braucht ihr Internet auf euren Linux VMs. Das stellt ihr mit **NAT** bereit.

**NAT** (**N**etwork **A**ddress **T**ranslation) ist eine Technik, um private IP-Adressen in öffentliche IP-Adressen umzuwandeln. Diese Technik wird hauptsächlich von Routern/Firewalls eingesetzt, die lokale Netzwerke mit dem Internet verbinden.

In einem typischen Heimnetzwerk haben die Clients private IP-Adressen. Diese privaten Adressen sind nur innerhalb des lokalen Netzwerks gültig und können nicht direkt von Servern im Internet angesprochen werden. Der Router im Netzwerk hat jedoch eine öffentliche IP-Adresse, die im Internet sichtbar und eindeutig ist. Wenn ein Client im lokalen Netzwerk auf das Internet zugreifen möchte, sendet es seine Anfrage an den Router. Der Router übersetzt dann die private IP-Adresse des Clients in seine eigene öffentliche IP-Adresse und sendet die Anfrage weiter.

Wenn die Antwort zurückkommt, wandelt der Router die öffentliche IP-Adresse wieder in die private Ziel IP-Adresse und sendet sie an den Client zurück. So können alle Geräte im lokalen Netzwerk das Internet über dieselbe öffentliche IP-Adresse nutzen, ohne dass jedes einzelne eine eigene öffentliche IP-Adresse benötigt.

![Überblick NAT](firewall_nat.svg)

Dazu hilt die Doku zu [NAT](https://docs.vyos.io/en/latest/configuration/nat/nat44.html) und mal wieder der [Quick Start Guide](https://docs.vyos.io/en/latest/quick-start.html).

{{< collapsible label="Lösung NAT setup" >}}

{{< code language="vyos" source="/vagrant/configs/vyos/vyos.cfg" id="nat">}}

{{< /collapsible >}}





