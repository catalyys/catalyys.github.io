---
title: "Challenge I"
date: 2024-09-24
lastmod: 2024-09-27
draft: true
description: "projekt challenge 1"
featureimage: "https://github.com/catalyys/catalyys.github.io/blob/main/assets/azubi_umgebung_setup.svg?raw=true"
tags: ["fisi", "übung", "projekt"]
type: "projekt"
series: ["Projekt"]
series_order: 4
showPagination: true
---

## Vorwort

Als erste Herausforderung habe ich eine *hoch professionelle* Anwendung geschrieben. Diese sollt ihr mit Docker zum laufen bringen.

Die Anwendung besteht aus 2 Containern. Eine Server Seite und eine Client Seite. Der Server soll in der **Prod** Umgebung laufen. Der Client wird dann in der **Test** Umgebung aufgebaut. 

Als guter Kollege, kann ich euch folgende Aussage geben:

> Soweit Ich weiß, muss Port 8081, 8082 und 9982 freigeschaltet werden in der Firewall.


## Setup

### Server

docker-compose Datei für den Server:
```yaml
services:
  turbine:
    container_name: azubi-fw-challenge
    image: catalyyst/azubi-fw-challenge:latest
    network_mode: "host"
```


### Client

docker-compose Datei für den Client:
```yaml
services:
  turbine:
    container_name: azubi-fw-challenge
    image: catalyyst/azubi-fw-challenge:latest
    command: ./azubi-fw-challenge client
    environment:
      SERVER_ADDRESS: "10.100.1.11"
```
> nicht vergessen, **SERVER_ADDRESS** zu ändern, auf die IP vom Docker Server.


{{< notice tip >}}
Das Log vom Container *kann* hilfreich sein.
Behaltet es im Auge.
{{< /notice >}}


## Challenge

Sobald der Client erfolgreich mit dem Server kommunizieren kann, wird das im Log angezeigt.

Ziel ist folgende Meldung im Client Log zu sehen:
```
Container vollständig verbunden
Glückwunsch du hast du Herausforderung geschafft!
```




