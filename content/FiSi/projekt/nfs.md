---
title: "IPv6"
date: 2024-09-19
lastmod: 2025-05-04
draft: true
description: "projekt ipv6"
featureimage: "https://github.com/catalyys/catalyys.github.io/blob/main/assets/project/azubi_umgebung_setup_v6.svg?raw=true"
tags: ["fisi", "übung", "projekt"]
type: "projekt"
series: ["Projekt"]
series_order: 7
showPagination: true
---


## Vorwort

Ziel ist es, einen **NFS** Server bereit zu stellen und ihn als zentralen Ort für Backups zu benutzen.
Passieren soll das in der **test** Umgebung.

---

## NFS Setup

### nfs konfigurieren allgemein

wichtige Dateien:
- `/etc/exports`

Die wichtigen Einstellungen sind alle in `/etc/exports`. Hier auch mal ein Beispiel Datei, um den Aufbau zu zeigen.
```bash
# Path     -      IP / Hostname - (options)
/srv/nfs4         hostname1(rw,sync,fsid=0) 192.168.10.3(rw,sync,nohide)
/srv/nfs4/home    192.168.10.3(rw,sync,nohide)
/srv/nfs4/export  *(rw,sync,nohide)
```

#### Troubleshooting

Zum Troubleshooting könnt ihr folgendes versuchen:
- `exportfs -arv` um nfs neu zu laden
- `cat /var/log/syslog`/ `tail -f /var/log/syslog` für logs
- `exportfs -v` um alle shares anzuzeigen
- `mount | grep nfs` um alle shares als client anzuzeigen


---

### nfs konfigurieren auf server2

### nfs auf server1 mounten

## Rsync

