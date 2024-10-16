---
title: "DHCP und DNS mit IPv6"
date: 2024-08-28
lastmod: 2024-09-10
draft: false
description: "dhcp und dns mit IPv6"
tags: ["fisi", "dns", "dhcp", "ipv6", "übung"]
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
3. *dhcp* konfigurieren
4. *bind* konfigurieren

## Ziele

1. einen *IPv6 dhcp* Server verwalten
2. *IPv6 bind* Zone pflegen
3. Systeme miteinander kommunizieren lassen

![Abbildung](dhcp_dns_ipv6_azubi.svg)

## Anleitung

### Installation

Zuerst muss *bind* und *dhcp* installiert werden. Mit folgendem Befehl könnt ihr alle notwendigen Dienste installieren.

```bash
apt install bind9 dnsutils isc-dhcp-server
```

---

{{% include "/FiSi/aufgaben/dhcp.md" "\*dhcp\* konfigurieren allgemein" %}}
{{% include "/FiSi/aufgaben/dhcp.md" "Beispiele" %}}
{{% include "/FiSi/aufgaben/dhcp.md" "Troubleshooting" %}}

{{% include "/FiSi/aufgaben/dns.md" "\*bind\* konfigurieren allgemein" %}}
{{% include "/FiSi/aufgaben/dns.md" "Troubleshooting" %}}

### *dhcp* konfigurieren auf *dc*

Zunächste müsst ihr euch informieren welche IPv6 Adressen es gibt und welche wir für das testen nehmen können.


{{< notice tip >}}
Es gibt wie bei IPv4 auch **private** IPv6 Adressen, diese werden zwar kaum benutzt, sind aber gut für Test Zwecke.
{{< /notice >}}


{{< collapsible label="Lösung dhcpd6.conf" >}}
>für unseren Zweck reichen die *Unique Local Unicast* Adressen mit einer Range von `fc00::/7`.
{{< /collapsible >}}

Die erste Aufgabe ist es, den *dhcp* Server auf *dc* zu konfigurieren. Dazu hat *dc* die IPv6 Adresse **fd11:2:3:4::10**. 
Für das Netz **fd11:2:3:4::/64** muss nun ein gültiger Eintrag in der `dhcpd6.conf` vorgenommen werden.

{{< collapsible label="Lösung dhcpd6.conf" >}}
 
```bash
subnet6 fd11:2:3:4::/64 {
		range6 fd11:2:3:4::100 fd11:2:3:4::254;
	    option dhcp6.name-servers fd11:2:3:4::10;
	    option dhcp6.domain-search "azubi.dataport.de";
}
```
{{< /collapsible >}}

**Was funktionieren sollte**:<br>
Mit den beiden Clients solltet ihr jetzt IPv6 Adressen bekommen.
Um die DHCP Sequenz zu starten könnt ihr den Befehl `dhclient -6 ens18` benutzen, dabei ist `ens18` das Interface, auf dem ihr eine neue Lease haben wollt.

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
root@ns1# dig +noall +answer mail.azubi.dataport.de @localhost

mail.azubi.dataport.de. 3600 IN CNAME dc.azubi.dataport.de.
dc.azubi.dataport.de. 3600 IN AAAA fd11:2:3:4::10
```

{{< collapsible label="Lösung azubi.dataport.de.zone" >}}
```dns
$ORIGIN azubi.dataport.de.
$TTL    3600
@       IN      SOA     ns1.azubi.dataport.de. root.azubi.dataport.de. (
                   2007010401           ; Serial
                         3600           ; Refresh [1h]
                          600           ; Retry   [10m]
                        86400           ; Expire  [1d]
                          600 )         ; Negative Cache TTL [1h]

@       IN      NS      ns1.azubi.dataport.de.

ns1     IN      A       fd11:2:3:4::10
dc    IN      A       fd11:2:3:4::10

 mail    IN      CNAME   dc
```
{{< /collapsible >}}

<br>

{{< collapsible label="Lösung named.conf" >}}

```dns
acl goodclients {
    localhost;
    localnets;
};

options {
  listen-on { 0.0.0.0; };
  directory "/var/cache/bind";

  dnssec-validation yes;
  allow-query { goodclients; };
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


