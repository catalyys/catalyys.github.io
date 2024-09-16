---
title: "IPv4"
date: 2024-09-16
lastmod: 2024-09-16
draft: false
description: "ipv4 überblick"
tags: ["fisi", "ipv4", "doku"]
type: "doku"
---

## Adressklassen

| Klasse | 1. Oktett     | Standard Netzmaske | Kommentar     |
| ------ | ------------- | ------------------ | ------------- |
| A      | **0**xxx xxxx | 255.0.0.0          | 0-127.x.x.x   |
| B      | **10**xx xxxx | 255.255.0.0        | 128-191.x.x.x |
| C      | **110**x xxxx | 255.255.255.0      | 192-223.x.x.x |
| D      | **1110** xxxx |                    | 224-239.x.x.x |
| E      | **1111 0**xxx |                    | Experimentell |

<br>


{{< katex >}}
### private IP-Adressbereiche

| Klasse | IP                            | Standard Netzmaske | Anzahl Hosts je Netz     | Suffix |
| ------ | ----------------------------- | ------------------ | ------------------------ | ------ |
| **A**      | 10.0.0.0 - 10.255.255.255     | 255.0.0.0          | $$ 2^{24}-2 $$           | **/8**     |
| **B**      | 172.16.0.0 - 172.31.255.255   | 255.240.0.0        | $$ 2^{20}-2 $$           | **/12**    |
| **C**      | 192.168.0.0 - 192.168.255.255 | 255.255.0.0        | $$ 2^{16}-2 $$           | **/16**    |

{{< collapsible label="binär Berechnungen Subnetz" >}}

|  notation | ergebnis | invers |
| --------- |:---:|:---:|
| $$2^{7}$$ | 128 | 128 |
| $$2^{6}$$ | 64  | 192 |
| $$2^{5}$$ | 32  | 224 |
| $$2^{4}$$ | 16  | 240 |
| $$2^{3}$$ |  8  | 248 |
| $$2^{2}$$ |  4  | 252 |
| $$2^{1}$$ |  2  | 254 |
| $$2^{0}$$ |  1  | 255 |

{{< /collapsible >}}


### Netzanteil und Broadcast

#### 192.168.43.91/24

Netzanteil &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp; *Hostanteil* <br>
**110**0 0000 **.** 1010 1000 **.** 0010 1011 **.** **|** *0101 1011*

255.255.255.0 (/24) <br>
1111 1111 **.** 1111 1111 **.** 1111 1111 **.** **|** *0000 0000*

**Netzadresse**:
Netzadresse = Hostanteil alles *0* <br>
1100 0000.1010 1000.0010 1011 **|**.*0000 0000* <br>
192.168.43.*0*

**Broadcastadresse**:
Netzadresse = Hostanteil alles *1* <br>
1100 0000.1010 1000.0010 1011 **|**.*1111 1111* <br>
192.168.43.*255*

2 Hosts mit dem selben **Netzanteil** können miteinander kommunizieren.

{{< alert >}}
Auch wenn die Netzmaske anders ist können 2 Hosts miteinander kommunizeiren.
*10.0.0.4/8* und *10.0.0.5/16* **können kommunizieren**, da sie beiden den gleichen Netzanteil bei der anderen Netzmaske haben.
{{< /alert >}}


### Subnetting

#### 172.16.160.0/20
- in 3 Subnetze aufteilen

172.16.160.0 <br>
1010 1100.0001 0000.1010 **|** *0000.0000 0000*

255.255.240.0 <br>
1111 1111.1111 1111.1111 **|** *0000.0000 0000*

$$2^{2}=4>3$$

*Subnetzmakse*:
255.255.252.0 <br>
1111 1111.1111 1111.1111 11 **|**_00.0000 0000_

| Subnetz | Netzadresse  | Subnetzmaske        | erste IP     | letzte IP      |
| ------- | ------------ | ------------------- | ------------ | -------------- |
| X       | 172.16.160.0 | 255.255.252.0 (/22) | 172.16.160.1 | 172.16.163.254 |
| Y       | 172.16.164.0 | 255.255.252.0 (/22) | 172.16.164.1 | 172.16.167.254 |
| Z       | 172.16.168.0 | 255.255.252.0 (/22) | 172.16.168.1 | 172.16.171.254 |


