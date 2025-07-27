---
title: "NFS"
date: 2024-09-19
lastmod: 2025-05-04
draft: false
description: "projekt nfs"
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

Der Aufbau soll wie folgt aussehen:

![NFS](project/azubi_nfs.svg)

Folgende Configs sollen per *rsync* auf den **NFS** Share kopiert werden:

- vyos
    - config backup
- server1
    - dns configs
    - docker compose Datei
- server2
    - dns configs
- server3
    - nur zum testen

### nfs konfigurieren allgemein

folgende Pakete werden benötigt:named

server: `sudo apt install nfs-kernel-server`

client: `sudo apt install nfs-common`

wichtige Dateien:

- `/etc/exports`

Die wichtigen Einstellungen sind alle in `/etc/exports`. Hier auch mal ein Beispiel Datei, um den Aufbau zu zeigen.

```bash
# Path     -      IP / Hostname - (options)
/srv/nfs4         hostname1(rw,sync,fsid=0) 192.168.10.3(rw,sync,nohide)
/srv/nfs4/home    192.168.10.0/24(rw,sync,nohide)
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

Geplant ist alle shares unter **/opt/nfs** zu verwalten. Den ersten Share kann dann *backup* heißen.
Der Ornder muss dann angelegt werden und ein entsprechender Eintrag in der `/etc/exports` muss existieren.

{{< collapsible label="Lösung /etc/exports" >}}

```export
/opt/nfs/backup 10.100.1.0/24(rw,sync,no_subtree_check,no_root_squash) 10.100.2.0/24(rw,sync,no_subtree_check,no_root_squash)
```

{{< /collapsible >}}

### nfs auf mounten

Nun muss der **NFS** Share auf *server1* und *server3* in `/mnt/backup` gemountet werden.
Das könnt ihr adhoc machen oder per fstab(`/etc/fstab`). fstab ist dabei permanent.

Adhoc ist gut, um Fehlermeldungen zu sehen, diese werden über fstab nicht gleich in der Console angezeigt.

{{< collapsible label="Lösung mounten" >}}

#### adhoc

```bash
sudo mount -t nfs server2.test.azubi.dataport.de:/opt/nfs/backup /mnt/backup
```

#### fstab

```fstab
server2.test.azubi.dataport.de:/opt/nfs/backup /mnt/backup nfs defaults,user,auto,relatime,rw 0 0
```

{{< /collapsible >}}

---

## Backup

Mit rsync sollen die Configs automatisch auf den backup share kopiert werden.
Die Scripte können auch komplett anders aussehen, das wichtige ist, dass am Ende die Dateien auf den **NFS** Share kopiert werden.

### bind

{{< collapsible label="Lösung rsync script" >}}

{{< code language="bash" source="/vagrant/configs/dns/bind_backup.sh">}}

{{< /collapsible >}}

Damit das regelmäßig ausgeführt wird, wird ein crontab Eintrag benötigt.

{{< collapsible label="Lösung crontab" >}}

Hier nicht vergessen die Datei ausfürbar zu machen.

```bash
chmod +x /root/bind_backup.sh
```

```crontab
*/15 * * * * /root/bind_backup.sh
```

{{< /collapsible >}}

### docker

{{< collapsible label="Lösung rsync script" >}}

{{< code language="bash" source="/vagrant/configs/docker/docker_backup.sh" >}}

{{< /collapsible >}}

Damit das regelmäßig ausgeführt wird, wird auch hier ein crontab Eintrag benötigt.

{{< collapsible label="Lösung crontab" >}}

Hier nicht vergessen die Datei ausfürbar zu machen.

```bash
chmod +x /root/docker_backup.sh
```

```crontab
*/15 * * * * /root/dokcer_backup.sh
```

{{< /collapsible >}}

### vyos

In VyOS kann man die Conifg über einen *archive* Ansatz auf *server2* kopieren, sobald man einen commit auslöst.
Unterstützt werden nur einige Protokolle, darunter leider kein *NFS*. *SCP* ist unter den Protokollen das einfachste für das Projekt.
Dafür muss ein backup User auf *server2* angelegt werden und ihm entsprechende Rechte gegeben werden.

{{< collapsible label="Lösung vyos" >}}

{{< code language="vyos" source="/vagrant/configs/vyos/vyos.cfg" id="config_archive" >}}

{{< /collapsible >}}

