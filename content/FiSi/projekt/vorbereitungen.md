---
title: "Vorbereitungen"
date: 2024-09-21
lastmod: 2024-09-22
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

## Vorbereitungen

2 Linux VMs können schon installiert werden und danach in ein privates Netz gepackt werden. und danach in ein privates Netz gepackt werden.

Dabei kommt eine VM in **prod** und eine in **test**.

![internes Netz](azubi_projekt_server.png "Einstellung in VirtualBox")

## Aufbau

Hier einmal eine Zeichnung, was aufgebaut werden soll.

![Netz Aufbau](azubi_umgebung_setup.svg "Netz Aufbau")


