---
title: "IPv6"
date: 2024-09-20
lastmod: 2025-05-04
draft: false
description: "projekt ipv6"
featureimage: "https://github.com/catalyys/catalyys.github.io/blob/main/assets/project/azubi_umgebung_setup_v6.svg?raw=true"
tags: ["fisi", "übung", "projekt"]
type: "projekt"
series: ["Projekt"]
series_order: 6
showPagination: true
---


## Vorwort

Ich empfehle euch zuerst zu IPv6 zu belesen und alle Wege, mit denen man IPv6-Adressen verteilen kann. Folgenden [Blogpost](https://metebalci.com/blog/hello-ipv6/) kann ich dazu empfehlen. Er sollte euch einen guten Einblick in IPv6 geben.


Den Beitrag von **Request for Comments** zu **IPv6** könnt ihr euch auch gerne anhören.
<iframe allow="autoplay *; encrypted-media *; fullscreen *; clipboard-write" frameborder="0" height="175" style="width:100%;max-width:660px;overflow:hidden;border-radius:10px;" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-storage-access-by-user-activation allow-top-navigation-by-user-activation" src="https://embed.podcasts.apple.com/de/podcast/rfce014-ipv6/id1082223939?i=1000401347741&l=en-GB"></iframe>


Hier auch nochmal eine Übersicht für SLAAC:
![SLAAC](ipv6_slaac.svg)


## IPv6 Setup

Zunächste müsst ihr euch informieren welche IPv6 Adressen es gibt und welche wir für das testen nehmen können.

{{< notice tip >}}
Es gibt wie bei IPv4 auch **private** IPv6 Adressen, diese werden zwar kaum benutzt, sind aber gut für Test Zwecke. Globale sind natürlich theoretisch auch möglich.
{{< /notice >}}

{{< collapsible label="Lösung IPv6 Bereich" >}}
>für unseren Zweck reichen die *Unique Local Unicast* Adressen mit einer Range von `fc00::/7`.
{{< /collapsible >}}

Für ein *IPv6*-Netz müsst ihr eine weitere VM erstellen. Die Umgebung soll **entw** heißen.
Wie bei den anderen beiden VMs, wird das Netzwerk Interface in das *interne Netzwerk* **entw** gepackt.
Bei VyOs wird dann auch noch ein weiterer Adapter im **entw** Netz hinzugefügt und die statische IP konfiguriert.

![Umgebung mit IPv6](project/azubi_umgebung_setup_v6.svg)

Damit ihr aus dem IPv6 Netz kommunizieren könnt, müsst ihr folgende Dinge erfüllt haben:
- NAT64
- DNS64


---

## NAT64

Im ersten Teil informiert ihr euch wieder zu NAT64 und warum es in der Umgebung notwendig ist.
Dazu kann ich die erste Hälfte des [Cisco Artikels](https://www.cisco.com/c/de_de/support/docs/ip/network-address-translation-nat/217208-understanding-nat64-and-its-configuratio.html) empfehlen.

Sobald ihr einen guten Überblick habt, könnt ihr **NAT64** in VyOs konfigurieren. Der [Guide](https://docs.vyos.io/en/latest/configuration/nat/nat64.html) von VyOs unterstützt euch dazu wieder.
Wichtig ist, ihr braucht kein *dns-forwarding* und habt auch keinen *translation-pool*, da ihr nur eine IP jeweils habt.

Wenn ihr damit fertig seid, könnt ihr die anderen *Clients* pingen.

```bash
root@bookworm ~# ping 64:ff9b::10.100.2.10
PING 64:ff9b::10.100.2.10(64:ff9b::a64:20a) 56 data bytes
64 bytes from 64:ff9b::a64:20a: icmp_seq=1 ttl=63 time=0.827 ms
64 bytes from 64:ff9b::a64:20a: icmp_seq=2 ttl=63 time=0.742 ms
64 bytes from 64:ff9b::a64:20a: icmp_seq=3 ttl=63 time=0.824 ms
64 bytes from 64:ff9b::a64:20a: icmp_seq=4 ttl=63 time=0.933 ms
```

{{< collapsible label="Lösung NAT64" >}}

{{< code language="vyos" source="/vagrant/configs/vyos/vyos.cfg" id="nat64">}}

{{< /collapsible >}}

---

## DNS64

Damit unser *NAT64 Präfix* automatisch vor die IPv4 Adressen gesetzt wird, brauchen wir DNS64.
Da wir auf **server3.entw.azubi.dataport.de** kein Internet haben, konfigurieren wir DNS64 auf **server1.prod.azubi.dataport.de**.

Auf **server3.entw.azubi.dataport.de** muss dann nur noch der DNS Server angepasst werden.

{{< collapsible label="Lösung DNS64" >}}

{{< code language="named" source="/vagrant/configs/dns/prod_named_v6.conf" id="dns64">}}

{{< /collapsible >}}

<br>

{{< collapsible label="Lösung /etc/resolv.conf" >}}

```bash
nameserver 64:ff9b::10.100.1.10
```

{{< /collapsible >}}

