---
title: "RA und DNS mit IPv6"
date: 2024-08-28
lastmod: 2024-11-10
draft: false
description: "ra und dns mit IPv6"
tags: ["fisi", "dns", "ra", "ipv6", "übung"]
featureimage: "https://github.com/catalyys/catalyys.github.io/blob/main/assets/dhcp_dns_ipv6_azubi.svg?raw=true"
type: "übung"
---

## Vorraussetzungen

- 3 Debian Server
	- 1 DHCP Server
	- 2 Clients

## grober Überblick der Arbeitsschritte

1. drei Linux VMs installieren
2. *dhcp* und *bind* installieren
3. *radvd* konfigurieren
4. *bind* konfigurieren

## Ziele

1. *IPv6 Router Advertisments* verwalten
2. *IPv6 bind* Zone pflegen
3. Systeme miteinander kommunizieren lassen

![Abbildung](dhcp_dns_ipv6_azubi.svg)

## Anleitung

Ich empfehle euch zuerst zu IPv6 zu belesen und alle Wege, mit denen man IPv6-Adressen verteilen kann. Folgenden [Blogpost](https://metebalci.com/blog/hello-ipv6/) kann ich dazu empfehlen. Er sollte euch einen guten Einblick in IPv6 geben.

Den Beitrag von **Request for Comments** zu **IPv6** könnt ihr euch auch gerne anhören.
<iframe allow="autoplay *; encrypted-media *; fullscreen *; clipboard-write" frameborder="0" height="175" style="width:100%;max-width:660px;overflow:hidden;border-radius:10px;" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-storage-access-by-user-activation allow-top-navigation-by-user-activation" src="https://embed.podcasts.apple.com/de/podcast/rfce014-ipv6/id1082223939?i=1000401347741&l=en-GB"></iframe>

### Installation

Zuerst muss *bind* und *radvd* installiert werden. Mit folgendem Befehl könnt ihr alle notwendigen Dienste installieren.

```bash
apt install bind9 dnsutils radvd
```

---

### *radvd* konfigurieren allgemein

wichtige Dateien:
- `/etc/radvd.conf`

In der `radvd.conf` Datei werden alle Einstellungen vorgenommen, welche für das *Router Advertisment* benötigt werden.

#### *radvd* Beispiele

```bash
interface enp9s0
{
	MinRtrAdvInterval 3;
	MaxRtrAdvInterval 4;
	AdvSendAdvert on;
	AdvManagedFlag on;
	prefix 2001:db8:1:0::/64
	{
		AdvValidLifetime 14300;
		AdvPreferredLifetime 14200; 
	};
};
```

#### *radvd* Troubleshooting

Zum Troubleshooting könnt ihr folgendes veruschen:

`journalctl -eu radvd.service` für logs

---

{{% include "/FiSi/aufgaben/dns.md" "\*bind\* konfigurieren allgemein" %}}
{{% include "/FiSi/aufgaben/dns.md" "Troubleshooting" %}}

### *radvd* konfigurieren auf *dc*

Zunächste müsst ihr euch informieren welche IPv6 Adressen es gibt und welche wir für das testen nehmen können.


{{< notice tip >}}
Es gibt wie bei IPv4 auch **private** IPv6 Adressen, diese werden zwar kaum benutzt, sind aber gut für Test Zwecke. Globale sind natürlich theoretisch auch möglich.
{{< /notice >}}


{{< collapsible label="Lösung dhcpd6.conf" >}}
>für unseren Zweck reichen die *Unique Local Unicast* Adressen mit einer Range von `fc00::/7`.
{{< /collapsible >}}

Die erste Aufgabe ist es, den **radvd** auf **dc** zu konfigurieren. Dazu bekommt **dc** die IPv6 Adresse **fd11:2:3:4::10**. 
Für den Prefix **fd11:2:3:4::/64** muss nun ein gültiger Eintrag in der `radvd.conf` vorgenommen werden.
Informiert euch, wie der DNS Server mit **radvd** übergeben wird.

{{< collapsible label="Lösung radvd.conf" >}}
 
```bash
interface eth0
{
	MinRtrAdvInterval 3;
	MaxRtrAdvInterval 4;
	AdvSendAdvert on;
	AdvManagedFlag on;
	prefix fd11:2:3:4::/64
	{
		AdvValidLifetime 14300;
		AdvPreferredLifetime 14200; 
	};
	RDNSS fd11:2:3:4::10 {};
};
```
{{< /collapsible >}}

**Was funktionieren sollte**:<br>
Mit den beiden Clients solltet ihr jetzt IPv6 Adressen bekommen (dies sollte komplett automatisch passieren).

---

### *bind* konfigurieren auf *dc*

Nun muss der *bind* auf *dc* konfiguriert werden. Das Ziel dabei soll es sein, Einträge aus `azubi.dataport.de` auflösen zu können. Dazu muss eine Zone generiert werden und die `named.conf` angepasst werden.
Um die Config zu validieren könnt ihr den Befehl `named-checkconf` verwenden. Bei der Zone hilft euch der Befehl `named-checkzone azubi.dataport.de /var/lib/bind/azubi.dataport.de.zone`.
In der `azubi.dataport.de` Zone soll es einen **ns1**, **dc** Eintrag geben und einen *CNAME* **mail** auf **dc**.
Dabei könnt ihr auch die beiden Clients im *DNS* nachpflegen mit der IPv6-Adresse, welche über *DHCP* erhalten wurde.

Anbei sind die Lösungen, falls ihr nicht mehr weiter wisst. Die Configs können auch anders aussehen und sind unten nur minimal/beispielhaft.

Zum testen eurer Umgebung könnt ihr den Befehl `dig` benutzen (`nslookup` ist auch möglich).

**Was funktionieren sollte**:

```bash
$ dig +short mail.azubi.dataport.de AAAA @fd11:2:3:4::10

dc.azubi.dataport.de.
fd11:2:3:4::10
```

{{< collapsible label="Lösung azubi.dataport.de.zone" >}}
```dns
$ORIGIN azubi.dataport.de.
$TTL    3600
@       IN      SOA     ns1.azubi.dataport.de. root.azubi.dataport.de. (
                   2007010401           ; Serial
                         3600           ; Refresh [1h]
                          600           ; Retry   [10m]
                        86400           ; Expire  [1d]
                          600 )         ; Negative Cache TTL [1h]

@     IN    NS      ns1.azubi.dataport.de.

ns1   IN    AAAA    fd11:2:3:4::10
dc    IN    AAAA    fd11:2:3:4::10

mail  IN    CNAME   dc
```
{{< /collapsible >}}

<br>

{{< collapsible label="Lösung named.conf" >}}

```dns
options {
  listen-on { any; };
  directory "/var/cache/bind";

  dnssec-validation yes;
  allow-query { any; };
};

zone "azubi.dataport.de" IN {
  type primary;
  file "/var/lib/bind/azubi.dataport.de.zone";
  allow-update { none; };
};
```
{{< /collapsible >}}

---

### ping testen

Als kleine Aufgabe, könnt ihr zuletzt versuchen von **client1** **client2** über den **DNS** Namen zu pingen.

{{< collapsible label="Lösung ping IPv6" >}}
```bash
root@client1# ping6 client2.azubi.dataport.de
root@client1# ping6 client2
root@client1# ping6 fd11:2:3:4::10
```
{{< /collapsible >}}


