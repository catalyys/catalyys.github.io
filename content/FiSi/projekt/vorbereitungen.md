---
title: "Vorbereitungen"
date: 2024-09-25
lastmod: 2024-10-22
draft: false
description: "projekt vorbereitung"
featureimage: "https://github.com/catalyys/catalyys.github.io/blob/main/assets/azubi_umgebung_setup.svg?raw=true"
tags: ["fisi", "übung", "projekt"]
type: "projekt"
series: ["Projekt"]
series_order: 1
showPagination: true
---


## Vorwort

Es werden 2 Linux VMs benötigt, dabei werde ich in den nachfolgenden Posts **Debian** verwenden. Ihr könnt gerne eine andere Distribution verwenden, dabei muss nur drauf geachtet werden, dass die Befehle anders sein könnten.

Desweiteren habe ich die Virtualisierung mit **VirtualBox** gemacht, falls ihr einen anderen Virtualisierer nehmen wollt, könnten hier auch einige Einstellungen anders sein.

Als Firewall habe ich mich erstmal für **VyOS** entschieden, hier gilt das gleiche.

Falls jemand sich für eine andere Firewall entscheidet, würde ich auch gerne eine Anleitung/Artikel damit veröffentlichen. Ihr könnt euch also gerne ausprobieren und dokumentieren.

Unter jedem Ausschnitt einer Datei, wird der Befehl stehen, mit dem ihr euch die komplette Datei herunterladen könnt.
Das herunterladen könnt ihr dann über `wget` direkt auf der VM machen.
In der Datei sind oft *START* und *END* Blöcke, diese sind nur Kommentare, damit ich den Code als Abschnitte hier im Blog verwenden kann. Diese können ignoriert oder rausgelöscht werden.

Die Configs sind alle getestet und sollten also funktionieren. Falls ihr Fehler findet, könnt ihr gerne ein Issue auf Github aufmachen.
Im [vagrant](https://github.com/catalyys/catalyys.github.io/tree/main/vagrant) Ordner befinden sich alle Configs und auch ein Vagrantfile + Ansible, um alle VMs automatisch zu provisionieren.
Dazu sind dort auch die Tests, welche mit pytest geschrieben sind. Dadurch könnt ihr auch eure Configs testen und vergleichen.

## Vorbereitungen

2 Linux VMs können schon installiert werden und danach in ein privates Netz gepackt werden.

Dabei kommt eine VM in **prod** und eine in **test**.

![internes Netz](azubi_projekt_server.png "Einstellung in VirtualBox")

Die Debian ISO bekommt ihr von [hier](https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/).

### apt

Falls ihr Internet haben wollt auf den VMs, bevor ihr die Firewall fertig habt, könnt ihr die VMs auch erstmal im NAT Netz lassen und eure Software (vim, curl, ...) installieren.

Wenn ihr die VMs im privaten Netz installiert habt, wird wahrscheinlich folgender Fehler erscheinen, wenn ihr `apt update` ausführt.

```shell
root@bookworm ~# apt update
Ign:1 cdrom://[Debian GNU/Linux 12.10.0 _Bookworm_ - Official amd64 DVD Binary-1 20230610-10:23] bookworm InRelease
Err:2 cdrom://[Debian GNU/Linux 12.10.0 _Bookworm_ - Official amd64 DVD Binary-1 20230610-10:23] bookworm Release
  Please use apt-cdrom to make this CD-ROM recognized by APT. apt-get update cannot be used to add new CD-ROMs
Reading package lists... Done
E: The repository 'cdrom://[Debian GNU/Linux 12 _Bookworm_ - Official amd64 DVD Binary-1 20230610-10:23] bookworm Release' does not have a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
```

![apt error](project/apt_error.png "apt Fehler wegen flaschen Repos")

Um den Fehler zu beheben, müsst ihr die Datei `/etc/apt/sources.list` anpassen und mit folgendem Inhalt füllen.

{{< code language="shell" source="/vagrant/configs/sources.list" >}}

## Aufbau

Hier einmal eine Zeichnung, was aufgebaut werden soll.

![Netz Aufbau](azubi_umgebung_setup.svg "Netz Aufbau")


