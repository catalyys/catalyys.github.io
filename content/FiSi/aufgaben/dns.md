---
title: "DNS"
date: 2024-08-23
lastmod: 2024-10-16
draft: false
description: "dns mit IPv4"
tags: ["fisi", "dns", "übung"]
featureimage: "https://github.com/catalyys/catalyys.github.io/blob/main/assets/dns_azubi.svg?raw=true"
type: "übung"
---


## grober Überblick der Arbeitsschritte

1. zwei Linux VMs installieren (Debian)
2. auf allen *bind* installieren
3. alle *bind* konfigurieren

## Ziele

1. zwei DNS Server miteinander verbinden und eine Kaskade bilden
2. alle DNS Aufrufe lassen sich von den DNS Servern aus auflösen

![DNS Abbildung](dns_azubi.svg)

## Anleitung

Diese Aufgabe setzt Debain vorraus. Mit entsprechenden Anpassungen ist alles mit anderen Distributionen möglich.
Die Installation vom Debian-System wird nicht behandelt. Dies muss alleine passieren.
Wenn alle Debian-VM's installiert sind und miteinander kommunizieren können, kann mit den Aufgaben begonnen werden.
Für Informationen empfehle ich die [bind9-Doku](https://bind9.readthedocs.io/en/latest/chapter1.html) und die [Debian-Doku](https://wiki.debian.org/Bind9).

### *bind* installieren

Mit folgendem Befehl könnt ihr *bind* und *dig* installieren:

```bash
apt install bind9 dnsutils
```

### *bind* konfigurieren allgemein

wichtige Dateien:
- `/etc/bind/named.conf`
- `/var/lib/bind/azubi.dataport.de.zone`

Bei Debian wird im Standart die `named.conf` in mehrere Dateien aufgespaltet. In dieser Übung ist das aber nicht notwendig, da wir nur eine kleine `named.conf` brauchen, die auch in einer Datei übersichtlich ist.
Falls ihr die Datei trotzdem aufteilen wollt, ist das mit dem `include`-Befehl möglich.

```ini
...
include "/etc/bind/named.conf.options";
...
```

#### Troubleshooting

Zum Troubleshooting könnt ihr folgendes versuchen:
- `journalctl -eu named.service` für logs
- `named-checkconf` um die `named.conf` zu validieren
- `named-checkzone azubi.dataport.de /var/lib/bind/azubi.dataport.de.zone` um die Zonen Config zu validieren

---

### *bind* konfigurieren auf *ns1*

Die erste Aufgabe ist es, *ns1* zu konfigurieren. Das Ziel dabei soll es sein, Einträge aus `azubi.dataport.de` auflösen zu können und auch vom Upstream DNS `google.de`. Dazu muss eine Zone generiert werden und die `named.conf` angepasst werden.
Um die Config zu validieren könnt ihr den Befehl `named-checkconf` verwenden. Bei der Zone hilft euch der Befehl `named-checkzone azubi.dataport.de /var/lib/bind/azubi.dataport.de.zone`.
In der `azubi.dataport.de` Zone soll es einen **ns1**, **server** Eintrag geben und einen *CNAME* **mail** auf **server**.
IP-Adressen könnt ihr euch dabei selbst ausdenken.

Anbei sind die Lösungen, falls ihr nicht mehr weiter wisst. Die Configs können auch anders aussehen und sind unten nur minimal/beispielhaft.

Zum testen eurer Umgebung könnt ihr den Befehl `dig` benutzen (`nslookup` ist auch möglich).

**Was funktionieren sollte**:
```bash
root@ns1# dig +noall +answer google.de @localhost

google.de. 283 IN A 142.250.181.195
```

```bash
root@ns1# dig +noall +answer mail.azubi.dataport.de @localhost

mail.azubi.dataport.de. 3600 IN CNAME server.azubi.dataport.de.
server.azubi.dataport.de. 3600 IN A 192.168.0.2
```

{{< collapsible label="Lösung azubi.dataport.de.zone" >}}
```bash
$ORIGIN azubi.dataport.de.
$TTL    3600
@       IN      SOA     ns1.azubi.dataport.de. root.azubi.dataport.de. (
                   2007010401           ; Serial
                         3600           ; Refresh [1h]
                          600           ; Retry   [10m]
                        86400           ; Expire  [1d]
                          600 )         ; Negative Cache TTL [1h]

@       IN      NS      ns1.azubi.dataport.de.

ns1     IN      A       192.168.0.1
server    IN      A       192.168.0.2

mail    IN      CNAME   server
```
{{< /collapsible >}}

<br>

{{< collapsible label="Lösung named.conf" >}}

```bash
options {
  listen-on { any; };
  directory "/var/cache/bind";

  forward only;
  forwarders { 1.1.1.1; };

  allow-query { any; };
};

zone "azubi.dataport.de" IN {
  type primary;
  file "/var/lib/bind/azubi.dataport.de.zone";
};
```

{{< /collapsible >}}

---

### *bind* konfigurieren auf *ns2*

Das ganze soll jetzt auch auf *ns2* passieren. Als Herausforderung für euch werde ich hier keine weiteren Informationen geben. Aus der Grafik sollte entnommen werden können, wie der Aufbau aussehen sollte.

Zum testen eurer Umgebung könnt ihr wieder den Befehl `dig` benutzen (`nslookup` ist auch möglich).

**Was funktionieren sollte**:
```bash
root@ns2# dig +noall +answer google.de @localhost

google.de. 78 IN A 142.250.180.67
```

```bash
root@ns2# dig +noall +answer mail.azubi.dataport.de @localhost

mail.azubi.dataport.de. 3600 IN CNAME server.azubi.dataport.de.
server.azubi.dataport.de. 3600 IN A 192.168.0.2
```

```bash
root@ns2# dig +noall +answer debian.olli.azubi.dataport.de @localhost

debian.olli.azubi.dataport.de. 3600 IN A 192.168.2.2
```

{{< collapsible label="Lösung olli.azubi.dataport.de.zone" >}}

```bash
$ORIGIN olli.azubi.dataport.de.
$TTL    3600
@       IN      SOA     ns2.olli.azubi.dataport.de. root.olli.azubi.dataport.de. (
                   2007010401           ; Serial
                         3600           ; Refresh [1h]
                          600           ; Retry   [10m]
                        86400           ; Expire  [1d]
                          600 )         ; Negative Cache TTL [1h]

@       IN      NS      ns2.olli.azubi.dataport.de.

ns2     IN      A       192.168.2.1
debian    IN      A       192.168.2.2
```

{{< /collapsible >}}

<br>

{{< collapsible label="Lösung named.conf" >}}

```bash
options {
  listen-on { any; };
  directory "/var/cache/bind";

  forward only;
  forwarders { 192.168.0.1; };

  allow-query { any; };
};

zone "olli.azubi.dataport.de" IN {
  type primary;
  file "/var/lib/bind/olli.azubi.dataport.de.zone";
};
```

{{< /collapsible >}}

---

### redirect Zone

Damit die *name*.azubi.dataport.de Zone auf dem *ns1* auflösbar ist, gibt es folgende Möglichkeiten:
1. eine secondary Zone
2. eine forward Zone auf *ns1*
Bei der secondary Zone muss die Config auf *ns1* **und** auf *ns2* angepasst werden. Eine forward Zone braucht nur eine Anpassung auf *ns1*. Daraus resultieren noch weitere Vor- und Nachteile. Beide Varianten haben aber die Anwendungszwecke.
Ihr könnt euch für eine der beiden Varianten entscheiden und diese dann einrichten. Lösungen haben ich für beide Varianten.

#### secondary Zone

Für eine secondary Zone müsst ihr auf *ns2* den Transfer der Zone erlauben. Danach könnt ihr die Zone auf *ns1* anlegen und transferieren.
Hier noch ein paar Befehle die euch helfen können:
- `rndc reload` um im *bind* einen reload der Zonen zu machen und damit einen Transfer der Zone

{{< collapsible label="Lösung named.conf ns1" >}}
```zone
...
zone "olli.azubi.dataport.de" IN {
  type secondary;
  file "/var/lib/bind/olli.azubi.dataport.de.saved";
  allow-notiy { 192.168.2.1; };
  primaries { 192.168.2.1; };
};
```

{{< /collapsible >}}

<br>

{{< collapsible label="Lösung named.conf ns2" >}}
>Wichtig ist hier, in der **Zone** die **serial** zu erhöhen bei jeder Änderung.

```zone
...
zone "olli.azubi.dataport.de" IN {
  type primary;
  file "/var/lib/bind/olli.azubi.dataport.de.zone";
  allow-update { none; };
  notify yes;
  also-notify { 192.168.0.1; };
  allow-transfer { 192.168.0.1; };
};
```

{{< /collapsible >}}

#### forward

Die forward Zone wird einfach auf *ns1* in der `named.conf` angelegt und schickt sämtliche Anfrage von der Domäne an den forwarder. 


{{< collapsible label="Lösung named.conf forward Zone" >}}

```bind
...
zone "olli.azubi.dataport.de" IN {
  type forward;
  forward only;
  forwarders { 192.168.2.1; };
};
```

{{< /collapsible >}}
