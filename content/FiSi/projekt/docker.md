---
title: "Docker"
date: 2024-09-22
lastmod: 2024-09-27
draft: false
description: "projekt docker"
featureimage: "https://github.com/catalyys/catalyys.github.io/blob/main/assets/azubi_umgebung_setup.svg?raw=true"
tags: ["fisi", "übung", "projekt"]
type: "projekt"
series: ["Projekt"]
series_order: 4
showPagination: true
---


## Docker Setup

Zuerst müsst Docker auf **server1** installieren.

Dazu könnt ihr euch eine Variante von der [offiziellen Doku](https://docs.docker.com/engine/install/debian/) aussuchen.

## Docker Run

Für den ersten Versuch kann man das Standard *nginx* Imgae starten.

`docker run` benutzt man eigentlich nicht, aber für das erste ist es ganz gut, das einmal gesehen zu haben.

{{< collapsible label="docker run command" >}}
Es gibt viele Möglichkeiten den Container zu starten. Der beste Test ist, ob *nginx* erreichbar ist.

In diesem Beispiel läuft *nginx* auf Port **8080** und man kann es mit dem Browser oder `curl` testen.

```bash
docker run -it --rm -d -p 8080:80 --name web nginx

# Zum testen mit curl
curl http://localhost:8080/
```
{{< /collapsible >}}


## Docker Compose

`docker-compose` wird eher genutzt, da dort die *config* in einer Datei bleibt und man damit mehr übersicht hat.

Die Aufgabe ist also, den `docker run` Befehl in eine **compose** Datei umzuwandeln.

Um eine Container mit `docker-compose` zu starten, könnt ihr im Ordner mit der `docker-compose.yml` Datei den Befehl `docker-compose up` ausführen.

{{< collapsible label="docker-compose.yml" >}}

{{< code language="yaml" source="/vagrant/configs/docker/docker-compose.yml" id="nginx">}}

{{< /collapsible >}}

Im zweiten Schritt, soll nun die **nginx** config angepasst werden.

Das macht man mit *volume mounts*.

Die folgende Datei (*server1.html*) soll mit **nginx** präsentiert werden:

{{< code language="html" source="/vagrant/configs/docker/server1.html">}}

Nginx kann mit `curl localhost:8080` getestet werden.

{{< collapsible label="docker-compose.yml mit volume" >}}

{{< code language="yaml" source="/vagrant/configs/docker/docker-compose.yml">}}

{{< /collapsible >}}

## Docker Produktion

Nun soll der **nginx** auch von **server2** aus erreichbar sein.

Nginx kann mit `curl 10.100.1.11:8080` getestet werden.

Bonuspunkte, wenn **nur** die Verbindung zum **nginx** auf **server1** funktioniert.

{{< collapsible label="Lösung Firewall" >}}

{{< code language="vyos" source="/vagrant/configs/vyos/vyos.cfg" id="firewall_8080">}}

{{< /collapsible >}}

Legt passend dazu einen DNS Namen an, damit die URL auch mit `curl nginx.azubi.dataport.de:8080` erreichbar ist.


