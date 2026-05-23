### Conexiones

```mermaid
graph LR
    PC-A[PC-A] --> S0[Switch S0]
    PC-B[PC-B] --> S0

    S0 --> ROUTER-MEX[Router MEX]

    ROUTER-MEX --> ROUTER-MTY[Router MTY]
    ROUTER-MTY --> PC-E[PC-E]
    ROUTER-MTY --> ROUTER-QRO[Router QRO]
    ROUTER-QRO --> ROUTER-GDG[Router GDG]

    ROUTER-GDG --> S1[Switch S1]

    S1 --> PC-C[PC-C]
    S1 --> PC-D[PC-D]

    style S0 fill:#d4f1f9,stroke:#333,stroke-width:2px
    style S1 fill:#d4f1f9,stroke:#333,stroke-width:2px
    style ROUTER-MEX fill:#ffe5ec,stroke:#333,stroke-width:2px
    style ROUTER-MTY fill:#ffe5ec,stroke:#333,stroke-width:2px
    style ROUTER-QRO fill:#ffe5ec,stroke:#333,stroke-width:2px
    style ROUTER-GDG fill:#ffe5ec,stroke:#333,stroke-width:2px

```

### Router MEX

Conexión con $MEX \rightarrow S0$ full duplex
`interface gig 0/0 10.10.10.254 255.255.255.0`

Conexión con $MEX \rightarrow MTY$
`interface serial 0/0/0 172.16.17.6 255.255.255.252`

**DHCP config**

```text
enable
configure terminal
ip dhcp excluded-address 10.10.10.254
ip dhcp pool LAN_MEX
 network 10.10.10.0 255.255.255.0
 default-router 10.10.10.254
exit

```
**OSPF config**

```text
router ospf 1
 network 10.10.10.0 0.0.0.255 area 0
 network 172.16.17.4 0.0.0.3 area 0
exit
```
**VPN IPsec config**

```text
enable
configure terminal

license boot module c2900 technology-package securityk9

crypto isakmp policy 10
 encr aes
 authentication pre-share
 group 2
 exit
crypto isakmp key MyKey address 172.16.3.10

crypto ipsec transform-set ESP-AES-SHA esp-aes esp-sha-hmac
 exit

crypto map VPN-ENTIKUS 10 ipsec-isakmp
 set peer 172.16.3.10
 set transform-set ESP-AES-SHA
 match address 100
 exit

interface Serial0/0/0
 crypto map VPN-ENTIKUS
 exit

ip route 0.0.0.0 0.0.0.0 Serial0/0/0
 exit

write memory
```

### Router MTY

Conexión con $MTY \rightarrow MEX$
`interface serial 0/0/0 172.16.17.5 255.255.255.252`

Conexión con $MTY \rightarrow QRO$
`interface serial 0/1/0 172.44.1.21 255.255.255.248`

Conexión con $MTY \rightarrow PC-E$
`interface gig 0/0 10.93.3.22 255.255.255.252`

**OSPF config**

```text
router ospf 1
 network 172.16.17.4 0.0.0.3 area 0
 network 172.44.1.16 0.0.0.7 area 0
 network 10.93.3.20 0.0.0.3 area 0
exit


```

### Router QRO

Conexión con $QRO \rightarrow MTY$
`interface serial 0/0/0 172.44.1.22 255.255.255.248`

Conexión con $QRO \rightarrow GDG$
`interface serial 0/1/0 172.16.3.9 255.255.255.252`

**OSPF config**

```text
router ospf 1
 network 172.44.1.16 0.0.0.7 area 0
 network 172.16.3.8 0.0.0.3 area 0
exit

```

### Router GDG

Conexión con $GDG \rightarrow S1$ full duplex
`interface gig 0/0 192.168.1.254 255.255.255.0`

Conexión con $GDG \rightarrow QRO$
`interface serial 0/0/0 172.16.3.10 255.255.255.252`

**DHCP config**

```text
enable
configure terminal
ip dhcp excluded-address 192.168.1.254
ip dhcp pool LAN_GDG
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.254
exit

```

**OSPF config**

```text
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
 network 172.16.3.8 0.0.0.3 area 0
exit

```

**VPN IPsec config**

```text
enable
configure terminal

license boot module c2900 technology-package securityk9

crypto isakmp policy 10
 encr aes
 authentication pre-share
 group 2
 exit
crypto isakmp key MyKey address 172.16.17.6

crypto ipsec transform-set ESP-AES-SHA esp-aes esp-sha-hmac
 exit

crypto map VPN-ENTIKUS-DASH 10 ipsec-isakmp
 set peer 172.16.17.6
 set transform-set ESP-AES-SHA
 match address 100
 exit

interface Serial0/0/0
 crypto map VPN-ENTIKUS-DASH
 exit

ip route 0.0.0.0 0.0.0.0 Serial0/0/0
 exit

write memory

```

### PC-A, PC-B, PC-C, PC-D
`IP Configuration: DHCP`

### PC-E

IPV4 Address
`10.93.3.21`
Subnet Mask
`255.255.255.252`
Default Gateway
`10.93.3.22`
