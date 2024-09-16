---
title: "DNS"
date: 2024-09-16
lastmod: 2024-09-16
draft: false
description: "dns Überblick"
tags: ["fisi", "dns", "doku"]
type: "doku"
---

{{< lead >}}
**D**omain **N**ame **S**ystem
{{< /lead >}}

## Aufgaben von DNS

1. Name zu IP -> *forward lookup*
2. IP zu Name -> *reverse lookup*
3. Dienstankündigung

## Übersicht

<div style="background-color:white; padding: 5px">
{{< mermaid >}}
graph LR
	A[NIC] --- B(Top Level Domain) & C(Länder Domain DENIC) & D(special)
	C --- .de

	.de --- .google
	.de --- .bs-technik-rostock
	.bs-technik-rostock --- ilias
	.bs-technik-rostock --- www

	C --- .tv
	C --- .it

	D --- .kinder
	D --- .amazon

	B --- .mil
	B --- .gov
	B --- .edu
	B --- .net
	B --- .com
{{< /mermaid >}}
</div>

<br>

<div style="background-color:white; padding: 10px">
{{< mermaid >}}
graph TD
    A[.] --- B(.com) & C(.de) & D(.org)
	B --- E(.fin02)
	E --- dc
	E --- www
	C --- F(.bs-technik-rostock)
	F --- ilias
	
	
	root --- X(TDL - Top Level Domain)
	X --- Y(SLD - Sub Level Domain) 
{{< /mermaid >}}
</div>

> ilias.bs-technik-rostock.de. = **FQDN** - **F**ully **Q**uallified **D**omain **N**ame 

## Einträge

| Typ                     | Beschreibung                                                            |
| ----------------------- | ----------------------------------------------------------------------- |
| A                       | Name zu IPv4                                                            |
| AAAA                    | Name zu IPv6                                                            |
| CNAME                   | Alias (Name zu Name)                                                    |
| MX                      | Mail Exchanger (Dienst)                                                 |
| PTR                     | Pointer (reverse lookup)                                                |
| SOA (start of athority) | Seriennummer, primärer Server, verantwortliche Person, Gültigkeitsdauer |
| NS                      | IP vom Nameserver(DNS)                                                  |



