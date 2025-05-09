---
title: "DNS"
date: 2024-09-23
lastmod: 2025-02-03
draft: false
description: "projekt dns"
featureimage: "https://github.com/catalyys/catalyys.github.io/blob/main/assets/azubi_umgebung_setup.svg?raw=true"
tags: ["fisi", "übung", "projekt"]
type: "projekt"
series: ["Projekt"]
series_order: 3
showPagination: true
---

## DNS Setup

Zunächste muss *bind* auf den beiden Linux VMs installiert werden. Danach erstellt ihr 2 Zonen und konfiguriert sie so, dass in beiden Netzwerken alle DNS Namen aufgelöst werden können.

{{% include "/FiSi/aufgaben/dns.md" "\*bind\* konfigurieren allgemein" %}}
{{% include "/FiSi/aufgaben/dns.md" "Troubleshooting" %}}

### *bind* konfigurieren auf *server1*

Die erste Aufgabe ist es, *server1* zu konfigurieren. Das Ziel dabei soll es sein, Einträge aus `azubi.dataport.de` auflösen zu können und auch vom Upstream DNS `google.de`. Dazu muss eine Zone generiert werden und die `named.conf` angepasst werden.
Um die Config zu validieren könnt ihr den Befehl `named-checkconf` verwenden. Bei der Zone hilft euch der Befehl `named-checkzone azubi.dataport.de /var/lib/bind/azubi.dataport.de.zone`.
In der `azubi.dataport.de` Zone soll es einen **server1**, **server** Eintrag geben und einen *CNAME* **mail** auf **server**.
IP-Adressen könnt ihr euch dabei selbst ausdenken.

Anbei sind die Lösungen, falls ihr nicht mehr weiter wisst. Die Configs können auch anders aussehen und sind unten nur minimal/beispielhaft.

Zum testen eurer Umgebung könnt ihr den Befehl `dig` benutzen (`nslookup` ist auch möglich).

**Was funktionieren sollte**:
```bash
root@server1# dig +short google.de @localhost

google.de. 283 IN A 142.250.181.195
```

```bash
root@server1# dig +short mail.azubi.dataport.de @localhost

mail.azubi.dataport.de. 3600 IN CNAME docker.azubi.dataport.de.
docker.azubi.dataport.de. 3600 IN A 10.100.1.9
```

{{< collapsible label="Lösung azubi.dataport.de.zone" >}}

{{< code language="zone" source="/vagrant/configs/dns/azubi.dataport.de.zone" id="zone">}}

{{< /collapsible >}}

<br>

{{< collapsible label="Lösung named.conf" >}}

{{< code language="bind" source="/vagrant/configs/dns/prod_named.conf" id="zone">}}

{{< /collapsible >}}

---

### *bind* konfigurieren auf *server2*

Das ganze soll jetzt auch auf *server2* passieren. Als Herausforderung für euch werde ich hier keine weiteren Informationen geben. Aus der Grafik sollte entnommen werden können, wie der Aufbau aussehen sollte.

{{< notice tip >}}
Denkt an die Firewall.
{{< /notice >}}

Zum testen eurer Umgebung könnt ihr wieder den Befehl `dig` benutzen (`nslookup` ist auch möglich).

**Was funktionieren sollte**:
```bash
root@server2# dig +short google.de @localhost

google.de. 78 IN A 142.250.180.67
```

```bash
root@server2# dig +short mail.azubi.dataport.de @localhost

mail.azubi.dataport.de. 3600 IN CNAME docker.azubi.dataport.de.
docker.azubi.dataport.de. 3600 IN A 10.100.1.9
```

```bash
root@server2# dig +short debian.test.azubi.dataport.de @localhost

debian.test.azubi.dataport.de. 3600 IN A 10.100.2.9
```

{{< collapsible label="Lösung test.azubi.dataport.de.zone" >}}

{{< code language="zone" source="/vagrant/configs/dns/test.azubi.dataport.de.zone" id="zone">}}

{{< /collapsible >}}

<br>

{{< collapsible label="Lösung named.conf" >}}

{{< code language="bind" source="/vagrant/configs/dns/test_named.conf" id="zone">}}

{{< /collapsible >}}

---

### redirect Zone

Damit die *name*.azubi.dataport.de Zone auf dem *server1* auflösbar ist, gibt es folgende Möglichkeiten:
1. eine secondary Zone
2. eine forward Zone auf *server1*
Bei der secondary Zone muss die Config auf *server1* **und** auf *server2* angepasst werden. Eine forward Zone braucht nur eine Anpassung auf *server1*. Daraus resultieren noch weitere Vor- und Nachteile. Beide Varianten haben aber die Anwendungszwecke.
Ihr könnt euch für eine der beiden Varianten entscheiden und diese dann einrichten. Lösungen haben ich für beide Varianten.

{{< collapsible label="Lösung Firewall" >}}

{{< code language="vyos" source="/vagrant/configs/vyos/vyos.cfg" id="firewall_dns">}}

{{< /collapsible >}}

#### secondary Zone

Für eine secondary Zone müsst ihr auf *server2* den Transfer der Zone erlauben. Danach könnt ihr die Zone auf *server1* anlegen und transferieren.
Hier noch ein paar Befehle die euch helfen können:
- `rndc reload` um im *bind* einen reload der Zonen zu machen und damit einen Transfer der Zone

{{< collapsible label="Lösung named.conf server1" >}}
```zone
...
zone "test.azubi.dataport.de" IN {
  type secondary;
  file "/var/lib/bind/test.azubi.dataport.de.saved";
  allow-notiy { 10.100.2.10; };
  primaries { 10.100.2.10; };
};
```

{{< /collapsible >}}

<br>

{{< collapsible label="Lösung named.conf server2" >}}
>Wichtig ist hier, in der **Zone** die **serial** zu erhöhen bei jeder Änderung.

```zone
...
zone "test.azubi.dataport.de" IN {
  type primary;
  file "/var/lib/bind/test.azubi.dataport.de.zone";
  allow-update { none; };
  notify yes;
  also-notify { 10.100.1.10; };
  allow-transfer { 10.100.1.10; };
};
```

{{< /collapsible >}}

#### forward

Die forward Zone wird einfach auf *server1* in der `named.conf` angelegt und schickt sämtliche Anfrage von der Domäne an den forwarder. 
Es wird dazu nur noch ein **NS** Eintrag für den nameserver in der anderen Domäne gebraucht.


{{< collapsible label="Lösung forward Zone" >}}

{{< code language="zone" source="/vagrant/configs/dns/azubi.dataport.de.zone" id="forward">}}

{{< code language="zone" source="/vagrant/configs/dns/prod_named.conf" id="forward">}}

{{< /collapsible >}}



