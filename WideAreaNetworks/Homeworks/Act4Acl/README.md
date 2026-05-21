<div align="center">

<img src="https://wiki.labnuevoleon.mx/images/4/4b/Tec-de-monterrey-logo.png" alt="Gymiq logo" width="400"/>

## INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY

**Campus Santa Fe**

# Actividad 4 ACL individual

### Implementación de redes de área amplia y servicios distribuidos

**Group 501**

Student
Ricardo Alfredo Calvo Pérez - A01028889

Professor
Jorge Rodríguez Ruiz

_April 2026_

</div>

**Realiza los siguiente:**

Crea e implementa una ACL que permita entrar el tráfico al servidor dns desde cualquier parte, así como el acceso web a la página `sitiob.com` solamente desde la red `172.16.10.0/24` y no permita pasar ningún otro tráfico hacia esa red en el router Red 30

Crea e implementa una ACL en el router Red 40 que solo permita pasar el tráfico de ping y web a sitioa desde cualquier dirección, pero bloqueando al host `172.16.20.2` de cualquier acceso.

**Responde las siguientes preguntas:**

- Si desde el router Red 30 quisieras permitir que solamente la red `172.16.10.0/24` tuviera acceso a la red interna con una access list standard, ¿Cuál sería esta access list?

El access list que necesitamos es un ACL estándar

- Si quisieramos permitir en el router Red 30 que solo las computadoras de la red `172.16.30.0/24` pudieran tener acceso a SSH al servidor DNS. ¿Se podría? En caso afirmativo, indica la access list. En caso negativo, justifica tu respuesta

No se puede implementar este acceso utilizando un ACL estándar, ya que este tipo de access lists solo permiten filtrar por dirección IP de origen y no por protocolo o puerto. Para que esto se pueda hacer se nececita una ACL extendida.

- Si quisieramos permitir en el router Red 30 que solo la computadoras de la red `172.16.30.0/24` pudieran tener acceso a SSH al servidor. ¿Se podría? En caso afirmativo, indica la access list. En caso negativo, justifica tu respuesta

Similar a la pregunta anterior, con un ACL estándar no se puede, pero con un ACL extendido si.
