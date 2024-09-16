---
title: "DHCP"
date: 2024-09-16
lastmod: 2024-09-16
draft: false
description: "dhcp Überblick"
tags: ["fisi", "dhcp", "doku"]
type: "doku"
---

{{< lead >}}
**D**ynamic **H**ost **C**onfiguration **P**rotocol
{{< /lead >}}

## Ablauf

<div style="background-color:white; padding: 10px">
{{< mermaid >}}
sequenceDiagram
	participant A as DHCP
	participant B as Client
    
	B ->> A: DHCP Discover (Broadcast)
	A ->> B: DHCP Offer (Unicast)
	B ->> A: DHCP Request (Unicast)
	A ->> B: DHCP Acknowledge (Unicast)

	B ->> A: DHCP Request (1/2 lease time)
	B ->> A: DHCP Request (3/4 lease time)
{{< /mermaid >}}
</div>

IP's können dynamisch oder statisch verteilt werden. Bei einer statischen Verteilung wird die IP mit einer MAC gebunden


## Was muss übergeben werden

- IP
- Netzmaske
- Leasetime

## Was kann übergeben werden

- Gateway
- NTP
- DNS IP
- Domain such suffix


