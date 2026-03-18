# Día 11 — Test Network: primera red Fabric en acción

---

## Slide 1 — Cotilleos 🗞️

[IMAGEN: Sección de cotilleos del mundo blockchain empresarial - formato de periódico sensacionalista]

[NOTA PROFESOR: Buscar 2-3 noticias recientes sobre despliegues de Hyperledger Fabric en producción, nuevas versiones, o casos de uso empresarial. Actualizar antes de cada edición del curso. Hoy es un día 100% práctico, así que los cotilleos deben ser breves (5 minutos máximo).]

---

## Slide 2 — El plan de hoy

**Hoy es el día más práctico del módulo.** No hay teoría nueva.

| Bloque | Actividad | Duración aprox. |
|--------|-----------|-----------------|
| 1 | Levantar test-network y explorar | 45 min |
| 2 | Desplegar y usar un chaincode | 45 min |
| 3 | Romper cosas a propósito | 30 min |
| 4 | Canal adicional y aislamiento | 30 min |
| 5 | CouchDB vs LevelDB | 30 min |
| 6 | Treasure Hunt: el detective de bloques | 30 min |
| 7 | Debate y quiz final del Módulo 1 | 45 min |

**Regla de hoy:** si algo falla, no te frustres. **Cada error es una oportunidad de aprender cómo funciona Fabric por dentro.**

[IMAGEN: Manos sobre un teclado con una terminal mostrando contenedores Docker de Fabric]

---

## Slide 3 — Portada sección

**Hyperledger Fabric**
Práctica 1: Levantar la red de pruebas

[IMAGEN: Interruptor gigante pasando de OFF a ON, con nodos de red Fabric iluminándose]

---

## Slide 4 — Práctica: Preparar el entorno

**Paso 1:** Abrir una terminal y navegar a test-network:
```bash
cd fabric-samples/test-network
```

**Paso 2:** Asegurarse de que no hay restos de ejecuciones anteriores:
```bash
./network.sh down
```

**Paso 3:** Verificar que Docker está limpio:
```bash
docker ps -a          # no debería haber contenedores de Fabric
docker volume ls      # no debería haber volúmenes de Fabric
docker network ls     # no debería haber redes fabric_test
```

[NOTA PROFESOR: Si hay restos de ejecuciones anteriores, el `./network.sh down` debería limpiarlos. Si no, usar `docker rm -f $(docker ps -aq)` y `docker volume prune -f` con PRECAUCIÓN (esto elimina TODOS los contenedores y volúmenes).]

---

## Slide 5 — Práctica: Levantar la red

**Paso 4:** Levantar la red y crear un canal:
```bash
./network.sh up createChannel
```

**¿Qué acaba de pasar?**
Este comando:
1. Generó el **material criptográfico** (certificados) para 2 organizaciones
2. Levantó **contenedores Docker** para peers y orderer
3. Creó un **canal** llamado `mychannel`
4. Unió los **peers** de ambas organizaciones al canal

**Paso 5:** Verificar que la red está corriendo:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Deberías ver:
- `peer0.org1.example.com`
- `peer0.org2.example.com`
- `orderer.example.com`

---

## Slide 6 — Práctica: Identificar los componentes

**Ejercicio:** para cada contenedor Docker, identificar su rol en la arquitectura que aprendimos en el día 9.

| Contenedor | Rol en Fabric | Puerto |
|-----------|--------------|--------|
| `peer0.org1.example.com` | Peer de la Organización 1 | 7051 |
| `peer0.org2.example.com` | Peer de la Organización 2 | 9051 |
| `orderer.example.com` | Nodo ordenador (ordering service) | 7050 |

**Preguntas para reflexionar:**
- ¿Cuántas organizaciones hay en esta red?
- ¿Cuántos peers tiene cada organización?
- ¿Cuántos orderers hay?
- ¿Qué pasaría si quisiéramos añadir una tercera organización?

**Paso 6:** Examinar los logs de un peer:
```bash
docker logs peer0.org1.example.com 2>&1 | head -50
```

[NOTA PROFESOR: En los logs se pueden ver mensajes de gossip (protocolo de comunicación entre peers), unión al canal, establecimiento de TLS, etc. No hace falta entender cada línea, pero sí identificar que el peer está comunicándose con otros componentes.]

---

## Slide 7 — Práctica: Explorar el material criptográfico

**Paso 7:** Explorar la estructura de directorios generada:
```bash
ls organizations/peerOrganizations/org1.example.com/
```

**Paso 8:** Verificar la estructura MSP que aprendimos ayer:
```bash
ls organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/msp/
```

Deberías ver las carpetas que estudiamos: `cacerts/`, `signcerts/`, `keystore/`, `tlscacerts/`

**Paso 9:** Leer el certificado del peer:
```bash
openssl x509 -in organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/msp/signcerts/peer0.org1.example.com-cert.pem -text -noout
```

**Identificar:**
- ¿Quién es el Subject (propietario)?
- ¿Quién es el Issuer (CA que lo emitió)?
- ¿Qué curva elíptica se usa?
- ¿Cuándo expira?

---

## Slide 8 — Práctica: Explorar el orderer

**Paso 10:** Explorar la estructura del orderer:
```bash
ls organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/
```

**Paso 11:** Comparar el certificado del orderer con el del peer:
```bash
openssl x509 -in organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/signcerts/orderer.example.com-cert.pem -text -noout
```

**Pregunta:** ¿El certificado del orderer fue emitido por la misma CA que el del peer de Org1?

[NOTA PROFESOR: No. El orderer tiene su propia CA (ordererOrg CA). Cada organización tiene su propia CA. Esto es fundamental: la CA de Org1 no puede emitir certificados válidos para Org2 ni para el orderer.]

---

## Slide 9 — Portada sección

**Hyperledger Fabric**
Práctica 2: Desplegar y usar un chaincode

[IMAGEN: Paquete de código siendo instalado en nodos de una red blockchain]

---

## Slide 10 — Práctica: Desplegar el chaincode

**Paso 1:** Desplegar el chaincode `asset-transfer-basic` escrito en Go:
```bash
./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-go -ccl go
```

**¿Qué acaba de pasar?** Este comando ejecutó el ciclo completo de despliegue:
1. **Package:** empaquetó el código del chaincode
2. **Install:** instaló el paquete en los peers de Org1 y Org2
3. **Approve:** cada organización aprobó la definición del chaincode
4. **Commit:** se hizo commit de la definición en el canal

**Paso 2:** Verificar que el chaincode está desplegado:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep basic
```

Deberías ver contenedores del chaincode corriendo (uno por cada peer).

[NOTA PROFESOR: El despliegue puede tardar 1-2 minutos porque Go necesita compilar el chaincode. Si falla, verificar que Go está instalado y que hay conectividad a internet para descargar dependencias.]

---

## Slide 11 — Práctica: Configurar variables de entorno

Para interactuar con la red como **Org1**, necesitamos configurar variables de entorno:

```bash
export PATH=${PWD}/../bin:$PATH
export FABRIC_CFG_PATH=${PWD}/../config/
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
```

**¿Qué hace cada variable?**
- `CORE_PEER_LOCALMSPID`: identifica a qué organización pertenecemos
- `CORE_PEER_MSPCONFIGPATH`: ruta al MSP del admin de Org1 (nuestro certificado y clave)
- `CORE_PEER_ADDRESS`: a qué peer nos conectamos
- `CORE_PEER_TLS_*`: configuración TLS para la conexión

[NOTA PROFESOR: Hacer énfasis en que ESTAS VARIABLES determinan "quiénes somos" en la red. Cambiarlas es como cambiar de identidad. Esto se usará más adelante para operar como Org2.]

---

## Slide 12 — Práctica: InitLedger — poblar el ledger

**Paso 3:** Inicializar el ledger con datos de ejemplo:
```bash
peer chaincode invoke -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel -n basic \
  --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
  -c '{"function":"InitLedger","Args":[]}'
```

**¿Por qué se envían dos `--peerAddresses`?**
- La política de endorsement requiere firma de **ambas organizaciones**
- El peer de Org1 (7051) y el peer de Org2 (9051) deben endorsar la transacción
- Esto es lo que hace Fabric diferente de Ethereum: el endorsement es explícito

Deberías ver: `Chaincode invoke successful. result: status:200`

---

## Slide 13 — Práctica: GetAllAssets — consultar el ledger

**Paso 4:** Consultar todos los assets del ledger:
```bash
peer chaincode query -C mychannel -n basic -c '{"Args":["GetAllAssets"]}'
```

**Resultado esperado** (formateado):
```json
[
  {"ID":"asset1","Color":"blue","Size":5,"Owner":"Tomoko","AppraisedValue":300},
  {"ID":"asset2","Color":"red","Size":5,"Owner":"Brad","AppraisedValue":400},
  {"ID":"asset3","Color":"green","Size":10,"Owner":"Jin Soo","AppraisedValue":500},
  {"ID":"asset4","Color":"yellow","Size":10,"Owner":"Max","AppraisedValue":600},
  {"ID":"asset5","Color":"black","Size":15,"Owner":"Adriana","AppraisedValue":700},
  {"ID":"asset6","Color":"white","Size":15,"Owner":"Michel","AppraisedValue":800}
]
```

**Diferencia clave con invoke:**
- `query` **no genera transacción** — solo lee datos del ledger local
- `invoke` **genera transacción** — pasa por endorsement, ordering y commit
- Es como la diferencia entre `view` y una función que modifica estado en Solidity

---

## Slide 14 — Práctica: TransferAsset — modificar el estado

**Paso 5:** Transferir un asset a un nuevo propietario:
```bash
peer chaincode invoke -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel -n basic \
  --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
  -c '{"function":"TransferAsset","Args":["asset6","Christopher"]}'
```

**Paso 6:** Verificar la transferencia:
```bash
peer chaincode query -C mychannel -n basic -c '{"Args":["ReadAsset","asset6"]}'
```

**Resultado esperado:**
```json
{"ID":"asset6","Color":"white","Size":15,"Owner":"Christopher","AppraisedValue":800}
```

El propietario cambió de "Michel" a "Christopher". La transacción pasó por endorsement de ambas organizaciones, fue ordenada y committed.

---

## Slide 15 — Práctica: Cambiar de organización

**Paso 7:** Ahora vamos a operar como **Org2**. Cambiar las variables de entorno:

```bash
export CORE_PEER_LOCALMSPID="Org2MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_ADDRESS=localhost:9051
```

**Paso 8:** Consultar el mismo asset desde Org2:
```bash
peer chaincode query -C mychannel -n basic -c '{"Args":["ReadAsset","asset6"]}'
```

**Pregunta:** ¿El resultado es el mismo que cuando consultamos desde Org1?

**Respuesta:** Sí. Ambas organizaciones comparten el **mismo ledger** en el canal `mychannel`. El estado es consistente.

**Paso 9:** Transferir un asset como Org2:
```bash
peer chaincode invoke -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel -n basic \
  --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
  -c '{"function":"TransferAsset","Args":["asset1","Elena"]}'
```

[NOTA PROFESOR: Insistir en que cambiar las variables de entorno cambia nuestra identidad. Es como si cambiáramos de usuario en un sistema. En una aplicación real, cada organización tendría su propia aplicación cliente con sus propias credenciales.]

---

## Slide 16 — Portada sección

**Hyperledger Fabric**
Práctica 3: Romper cosas a propósito

[IMAGEN: Martillo de pruebas golpeando suavemente una red blockchain, con fragmentos saliendo de los nodos]

---

## Slide 17 — Experimento 1: Invocar sin endorsement de ambas orgs

**¿Qué pasa si solo enviamos a un peer?**

Primero, volver a configurar como Org1:
```bash
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
```

Ahora intentar un invoke enviando solo al peer de Org1 (sin Org2):
```bash
peer chaincode invoke -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel -n basic \
  --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  -c '{"function":"TransferAsset","Args":["asset2","Hacker"]}'
```

**Resultado esperado:** La transacción será rechazada porque la política de endorsement requiere firmas de ambas organizaciones ("AND('Org1MSP.peer','Org2MSP.peer')").

**Lección:** en Fabric, las reglas de endorsement se respetan siempre. No puedes saltártelas.

[NOTA PROFESOR: El error puede variar según la versión de Fabric. Puede ser un error inmediato de validación de endorsement o puede fallar en la fase de commit. Examinar el error con los alumnos y buscar el mensaje relevante.]

---

## Slide 18 — Experimento 2: ¿Qué pasa si el orderer cae?

**Paso 1:** Detener el orderer:
```bash
docker stop orderer.example.com
```

**Paso 2:** Intentar hacer un invoke:
```bash
peer chaincode invoke -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel -n basic \
  --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
  -c '{"function":"TransferAsset","Args":["asset3","Test"]}'
```

**Resultado esperado:** Error de conexión al orderer. La transacción no se puede completar.

**Paso 3:** ¿Y las consultas?
```bash
peer chaincode query -C mychannel -n basic -c '{"Args":["GetAllAssets"]}'
```

**Resultado esperado:** La consulta **sí funciona** porque solo lee el ledger local del peer.

**Paso 4:** Restaurar el orderer:
```bash
docker start orderer.example.com
```

**Lección:** sin orderer no hay nuevas transacciones, pero las consultas siguen funcionando. El orderer es crítico para escrituras pero no para lecturas.

---

## Slide 19 — Experimento 3: Usar certificado de otra organización

**¿Qué pasa si configuramos las variables de Org1 pero usamos el MSP de Org2?**

```bash
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
```

Intentar una consulta:
```bash
peer chaincode query -C mychannel -n basic -c '{"Args":["GetAllAssets"]}'
```

**Resultado esperado:** Error. Estamos diciendo que somos Org1MSP pero presentando un certificado emitido por la CA de Org2. El peer detecta la inconsistencia.

**Restaurar la configuración correcta antes de continuar:**
```bash
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
```

**Lección:** en Fabric no puedes suplantar a otra organización. El certificado debe coincidir con el MSP declarado.

---

## Slide 20 — Experimento 4: Consultar un canal al que no perteneces

**Intentar consultar un canal inexistente:**
```bash
peer chaincode query -C canalfalso -n basic -c '{"Args":["GetAllAssets"]}'
```

**Resultado esperado:** Error. El peer no pertenece a ese canal.

**Lección:** la arquitectura de canales de Fabric garantiza el aislamiento. Un peer solo tiene acceso a los canales a los que se ha unido explícitamente.

[NOTA PROFESOR: Resumir las 4 lecciones de los experimentos:
1. Las políticas de endorsement son obligatorias
2. El orderer es crítico para escrituras pero no para lecturas
3. No puedes suplantar identidades de otras organizaciones
4. Los canales están aislados entre sí
Estas propiedades son fundamentales para entender la seguridad de Fabric.]

---

## Slide 21 — Portada sección

**Hyperledger Fabric**
Práctica 4: Canal adicional y aislamiento

[IMAGEN: Dos tubos transparentes paralelos con datos diferentes fluyendo por cada uno, representando canales aislados]

---

## Slide 22 — Práctica: Crear un segundo canal

**Paso 1:** Crear un canal adicional llamado `canal2`:
```bash
./network.sh createChannel -c canal2
```

**Paso 2:** Verificar que el peer está ahora en dos canales:
```bash
peer channel list
```

**Resultado esperado:**
```
Channels peers has joined:
mychannel
canal2
```

**Paso 3:** Desplegar un chaincode diferente en canal2:
```bash
./network.sh deployCC -ccn basic2 -ccp ../asset-transfer-basic/chaincode-go -ccl go -c canal2
```

[NOTA PROFESOR: Usamos el mismo código Go pero con un nombre diferente (basic2). En una red real, cada canal podría tener chaincodes completamente distintos.]

---

## Slide 23 — Práctica: Verificar aislamiento entre canales

**Paso 4:** Inicializar el ledger en canal2:
```bash
peer chaincode invoke -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C canal2 -n basic2 \
  --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
  -c '{"function":"InitLedger","Args":[]}'
```

**Paso 5:** Consultar en canal2:
```bash
peer chaincode query -C canal2 -n basic2 -c '{"Args":["GetAllAssets"]}'
```

**Paso 6:** Comparar con mychannel (donde ya hicimos transferencias):
```bash
peer chaincode query -C mychannel -n basic -c '{"Args":["ReadAsset","asset6"]}'
```

**Observación clave:** en `canal2`, asset6 pertenece a "Michel" (datos originales). En `mychannel`, asset6 pertenece a "Christopher" (lo transferimos antes). **Los canales son mundos completamente independientes.**

---

## Slide 24 — Portada sección

**Hyperledger Fabric**
Práctica 5: CouchDB vs LevelDB

[IMAGEN: Dos bases de datos lado a lado: una minimalista (LevelDB) y otra con interfaz web rica (CouchDB)]

---

## Slide 25 — Práctica: Red con CouchDB

**Paso 1:** Destruir la red actual y crear una nueva con CouchDB:
```bash
./network.sh down
./network.sh up createChannel -s couchdb
```

**Paso 2:** Verificar que hay contenedores CouchDB corriendo:
```bash
docker ps --format "table {{.Names}}\t{{.Ports}}" | grep couch
```

Deberías ver:
- `couchdb0` (para peer de Org1) — puerto 5984
- `couchdb1` (para peer de Org2) — puerto 7984

**Paso 3:** Desplegar el chaincode en la nueva red:
```bash
./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-go -ccl go
```

---

## Slide 26 — Práctica: Explorar CouchDB

**Paso 4:** Abrir la interfaz web de CouchDB en el navegador:
```
http://localhost:5984/_utils/
```

**Credenciales:** admin / adminpw

**Paso 5:** Inicializar datos y explorar:
```bash
# Configurar variables de Org1 primero (ver slide 11)
peer chaincode invoke -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel -n basic \
  --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
  -c '{"function":"InitLedger","Args":[]}'
```

**Paso 6:** En la interfaz web de CouchDB:
1. Buscar la base de datos `mychannel_basic`
2. Explorar los documentos — son los assets del chaincode
3. Observar que cada asset es un documento JSON completo
4. Probar a buscar por campos (ej: todos los assets de color "blue")

---

## Slide 27 — CouchDB vs LevelDB: Comparativa

| Aspecto | LevelDB | CouchDB |
|---------|---------|---------|
| **Tipo** | Key-value store | Base de datos documental (JSON) |
| **Consultas** | Solo por clave exacta | Consultas ricas por campos (JSON queries) |
| **Interfaz web** | No tiene | Sí (Fauxton en puerto 5984) |
| **Rendimiento** | Más rápido para lecturas por clave | Algo más lento, pero más versátil |
| **Índices** | Solo la clave | Índices personalizados sobre cualquier campo |
| **Uso recomendado** | Cuando solo necesitas leer por ID | Cuando necesitas buscar por propiedades |
| **Configuración** | Por defecto | Requiere flag `-s couchdb` |

**Ejemplo de JSON query (solo posible con CouchDB):**
```json
{
  "selector": {
    "Color": "blue",
    "Size": {"$gt": 5}
  }
}
```

[NOTA PROFESOR: En LevelDB, para buscar "todos los assets azules" tendrías que recorrer todos los assets y filtrar. Con CouchDB, puedes hacer la consulta directamente. Esto es especialmente útil cuando el volumen de datos es grande.]

---

## Slide 28 — Portada sección

**Hyperledger Fabric**
Treasure Hunt: El detective de bloques 🔍

[IMAGEN: Lupa sobre una blockchain, con transacciones y logs destacados como pistas de una investigación]

---

## Slide 29 — Treasure Hunt: El detective de bloques

**Escenario:** Eres el administrador de la red Fabric de un consorcio logístico. Un usuario reporta que intentó transferir el asset5 a "Roberto" pero el cambio no se refleja en el ledger.

**Tu misión:** Investigar qué pasó usando las herramientas de Fabric.

**Pistas y comandos que necesitarás:**

**Pista 1 — Verificar el estado actual del asset:**
```bash
peer chaincode query -C mychannel -n basic -c '{"Args":["ReadAsset","asset5"]}'
```
¿Quién es el propietario actual? ¿Se hizo la transferencia o no?

**Pista 2 — Consultar la altura del blockchain:**
```bash
peer channel getinfo -c mychannel
```
¿Cuántos bloques hay? ¿Es consistente con el número de transacciones que hemos hecho?

**Pista 3 — Examinar los logs del peer:**
```bash
docker logs peer0.org1.example.com 2>&1 | grep -i "error\|fail\|reject" | tail -20
```
¿Hay errores de validación o endorsement?

---

## Slide 30 — Treasure Hunt: Resolución

**Pista 4 — Intentar reproducir la transacción:**
```bash
peer chaincode invoke -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel -n basic \
  --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
  -c '{"function":"TransferAsset","Args":["asset5","Roberto"]}'
```

**Pista 5 — Verificar el resultado:**
```bash
peer chaincode query -C mychannel -n basic -c '{"Args":["ReadAsset","asset5"]}'
```

**Conclusión del caso:** La transacción original probablemente falló por una de estas razones:
- No se incluyeron los peers de ambas organizaciones (fallo de endorsement)
- Se usaron credenciales incorrectas
- El orderer no estaba disponible en ese momento

**Herramientas clave del detective de bloques:**
- `peer chaincode query`: verificar estado actual
- `peer channel getinfo`: altura y hash del blockchain
- `docker logs`: examinar logs de componentes
- `peer channel fetch`: obtener bloques específicos para auditoría

[NOTA PROFESOR: El objetivo no es que encuentren un bug real, sino que practiquen el proceso de investigación y se familiaricen con las herramientas de diagnóstico. Estas habilidades son fundamentales para operar una red Fabric en producción.]

---

## Slide 31 — Portada sección

**Hyperledger Fabric**
Cierre del Módulo 1: Debate y evaluación

[IMAGEN: Mesa redonda de debate con participantes y una pizarra que muestra "EVM vs Fabric" con flechas entre ambos]

---

## Slide 32 — Debate: EVM vs Fabric — reflexiones finales

Después de 11 días comparando el mundo EVM con Hyperledger Fabric, discutir en grupo:

**1. ¿Qué fue lo más sorprendente al comparar EVM con Fabric?**
- ¿Esperaban tantas diferencias en el modelo de identidad?
- ¿La complejidad del despliegue frente a la simplicidad de Remix?

**2. ¿Qué parece más complejo?**
- ¿Fabric por su arquitectura de canales, endorsement y MSP?
- ¿O EVM por la gestión de gas, seguridad de smart contracts y MEV?

**3. ¿Dónde veis más potencial para vuestra empresa o sector?**
- ¿Trazabilidad de cadena de suministro?
- ¿Gestión de identidad y credenciales?
- ¿Tokenización de activos?
- ¿Compartir datos entre competidores de forma controlada?

**4. Si tuvierais que elegir una tecnología para un proyecto empresarial, ¿cuál elegiríais y por qué?**

[NOTA PROFESOR: No hay respuesta correcta. El objetivo es que articulen pros y contras con conocimiento de causa. Guiar hacia la conclusión de que la elección depende del caso de uso: Fabric brilla en redes permisionadas con múltiples organizaciones que necesitan privacidad; EVM brilla en ecosistemas abiertos y tokenización.]

---

## Slide 33 — Quiz final del Módulo 1: Blockchain general (preguntas 1-10)

**1.** ¿Qué problema resuelve el algoritmo de consenso en una blockchain?
a) La velocidad de las transacciones
b) El doble gasto y el acuerdo entre nodos
c) La encriptación de los datos
d) La compresión de los bloques

**2.** ¿Qué garantiza una función hash criptográfica?
a) Que los datos se pueden recuperar a partir del hash
b) Integridad: cualquier cambio en la entrada produce un hash completamente distinto
c) Que el hash siempre tiene el mismo tamaño que la entrada
d) Que dos entradas distintas siempre producen el mismo hash

**3.** En un sistema de criptografía asimétrica, ¿qué se usa para firmar una transacción?
a) La clave pública
b) La clave privada
c) El hash de la transacción
d) La dirección del wallet

**4.** ¿Cuál es la diferencia principal entre una blockchain pública y una permisionada?
a) Las públicas son más rápidas
b) Las permisionadas no usan criptografía
c) En las públicas cualquiera puede participar; en las permisionadas se requiere autorización
d) Las permisionadas no tienen consenso

**5.** ¿Qué es un smart contract?
a) Un contrato legal digitalizado
b) Código que se ejecuta automáticamente en la blockchain cuando se cumplen condiciones
c) Un acuerdo entre dos wallets
d) Un tipo de token

---

## Slide 34 — Quiz final del Módulo 1: Blockchain general (preguntas 6-10)

**6.** ¿Qué mecanismo de consenso usa Ethereum actualmente?
a) Proof of Work
b) Proof of Stake
c) PBFT
d) Raft

**7.** ¿Qué es el gas en Ethereum?
a) El combustible que alimenta los servidores
b) La unidad que mide el coste computacional de ejecutar transacciones
c) Un tipo de criptomoneda
d) El tiempo que tarda una transacción

**8.** ¿Qué es una CBDC?
a) Una criptomoneda descentralizada
b) Una moneda digital emitida por un banco central
c) Un token ERC-20
d) Un tipo de stablecoin privada

**9.** ¿Cuál de estas NO es una característica de una blockchain?
a) Inmutabilidad
b) Transparencia (en redes públicas)
c) Posibilidad de borrar transacciones por un administrador
d) Distribución entre múltiples nodos

**10.** ¿Qué es una DAO?
a) Una base de datos autónoma
b) Una organización gobernada por smart contracts y votación de sus miembros
c) Un tipo de exchange descentralizado
d) Un protocolo de préstamos

---

## Slide 35 — Quiz final del Módulo 1: Hyperledger Fabric (preguntas 11-15)

**11.** ¿Cuál es el flujo correcto de una transacción en Fabric?
a) Ordenar → Ejecutar → Validar
b) Ejecutar → Ordenar → Validar (Execute-Order-Validate)
c) Validar → Ejecutar → Ordenar
d) Ejecutar → Validar → Ordenar

**12.** ¿Qué componente emite los certificados X.509 en Fabric?
a) El peer
b) El orderer
c) La Certificate Authority (CA)
d) El chaincode

**13.** ¿Qué es un canal en Hyperledger Fabric?
a) Un tipo de smart contract
b) Una subred privada donde un grupo de organizaciones comparte un ledger independiente
c) El protocolo de comunicación entre peers
d) Un canal de chat entre administradores

**14.** ¿Qué contiene la carpeta `keystore/` del MSP?
a) Los certificados de las CAs de confianza
b) La clave privada de la identidad
c) Los certificados de los administradores
d) La configuración del canal

**15.** ¿Por qué `cryptogen` NO debe usarse en producción?
a) Porque es muy lento
b) Porque genera material criptográfico estáticamente, sin CA real para gestión dinámica de identidades
c) Porque solo funciona con Go
d) Porque no soporta TLS

---

## Slide 36 — Quiz final del Módulo 1: Hyperledger Fabric (preguntas 16-20)

**16.** ¿Cuál es la diferencia entre `peer chaincode invoke` y `peer chaincode query`?
a) invoke es más rápido que query
b) invoke genera una transacción que modifica el estado; query solo lee sin modificar
c) query requiere endorsement de múltiples organizaciones; invoke no
d) No hay diferencia, son sinónimos

**17.** ¿Qué pasa si el orderer está caído?
a) No se pueden hacer ni lecturas ni escrituras
b) No se pueden hacer nuevas transacciones (escrituras) pero las consultas (lecturas) siguen funcionando
c) La red se repara automáticamente
d) Los peers asumen el rol de orderer

**18.** ¿Qué ventaja ofrece CouchDB sobre LevelDB como state database?
a) Mayor velocidad en todas las operaciones
b) Consultas ricas por campos JSON, no solo por clave
c) Mejor compresión de datos
d) No requiere Docker

**19.** ¿Qué es Mutual TLS (mTLS) en Fabric?
a) Una forma de cifrar los chaincodes
b) Autenticación bidireccional donde ambas partes verifican el certificado de la otra
c) Un tipo de canal privado
d) El protocolo de consenso de Fabric

**20.** ¿Qué sucede si intentas presentar un certificado de Org2 diciendo que eres Org1?
a) La red acepta la transacción normalmente
b) La red detecta la inconsistencia entre el MSP declarado y el certificado, y rechaza la operación
c) El certificado se revoca automáticamente
d) Se crea una nueva organización

---

## Slide 37 — Respuestas del quiz

| Pregunta | Respuesta | Pregunta | Respuesta |
|----------|-----------|----------|-----------|
| 1 | b) El doble gasto y el acuerdo | 11 | b) Execute-Order-Validate |
| 2 | b) Integridad | 12 | c) Certificate Authority |
| 3 | b) La clave privada | 13 | b) Subred privada con ledger independiente |
| 4 | c) Pública = abierta; permisionada = autorizada | 14 | b) La clave privada |
| 5 | b) Código autoejecutado en blockchain | 15 | b) Material estático, sin CA real |
| 6 | b) Proof of Stake | 16 | b) invoke modifica; query solo lee |
| 7 | b) Coste computacional | 17 | b) Sin escrituras; lecturas sí |
| 8 | b) Moneda digital de banco central | 18 | b) Consultas ricas por campos JSON |
| 9 | c) Borrar transacciones | 19 | b) Autenticación bidireccional |
| 10 | b) Organización gobernada por smart contracts | 20 | b) Rechaza por inconsistencia MSP |

[NOTA PROFESOR: Revisar las respuestas en grupo. Si hay preguntas con baja tasa de acierto, dedicar unos minutos a reexplicar el concepto. Las preguntas 11-20 son específicas de Fabric — si los alumnos aciertan la mayoría, el módulo ha cumplido su objetivo.]

---

## Slide 38 — Limpieza del entorno

Antes de cerrar el día, limpiar el entorno:

```bash
cd fabric-samples/test-network
./network.sh down
```

Verificar que todo está limpio:
```bash
docker ps -a                # no debería haber contenedores de Fabric
docker volume ls            # limpiar si quedan volúmenes
docker network ls           # limpiar si queda fabric_test
```

---

## Slide 39 — ¿Qué viene en el Módulo 2?

**Módulo 2: Desarrollo de chaincodes y aplicaciones**

En las próximas sesiones:
- Anatomía de un chaincode en Go
- Escribir nuestro primer chaincode desde cero
- Ciclo de vida del chaincode: package, install, approve, commit
- Fabric Gateway SDK: aplicaciones cliente
- Eventos y notificaciones
- Private data collections
- Patrones avanzados

**Pasamos de USAR Fabric a CONSTRUIR sobre Fabric.**

[IMAGEN: Evolución visual de un usuario ejecutando comandos a un desarrollador escribiendo código de chaincode]

[NOTA PROFESOR: Cerrar el módulo reconociendo el esfuerzo de los alumnos. Han pasado de no saber nada sobre blockchain a levantar una red Fabric, desplegar chaincodes y ejecutar transacciones. Es un logro significativo. El Módulo 2 será más exigente en programación.]

---

## Actividad de relleno (si sobra tiempo)

### Fabric freestyle: modifica el chaincode (45-60 min)

- Los alumnos ya tienen la test-network funcionando con asset-transfer-basic desplegado.
- Reto: modificar el chaincode para añadir una funcionalidad nueva. Opciones a elegir:
  1. **Añadir un campo "Timestamp"** a cada asset que se registre automáticamente con la hora de creación.
  2. **Añadir una función "GetAssetHistory"** que devuelva el historial de cambios de un asset (usando la API de historial de Fabric: `GetHistoryForKey`).
  3. **Añadir una función "TransferWithApproval"** donde la transferencia requiere que el receptor confirme la recepción (dos transacciones).
  4. **Añadir validación de negocio:** un asset no puede tener un AppraisedValue negativo, y el Size debe estar entre 1 y 100.
- Pasos:
  1. Editar el código del chaincode (Go o JavaScript, según lo que desplegaron)
  2. Empaquetar la nueva versión
  3. Seguir el lifecycle completo: install → approve (ambas orgs) → commit
  4. Probar la nueva funcionalidad con invoke/query
- Si no da tiempo a completar el lifecycle, al menos que modifiquen el código y expliquen qué cambiarían.

[NOTA PROFESOR: La opción 4 (validación de negocio) es la más sencilla. La opción 2 (historial) es la más interesante porque muestra una capacidad que Ethereum no tiene fácilmente. Tener preparados snippets de código para cada opción por si los alumnos se atascan. Esta actividad es el puente perfecto al módulo 2, donde crearán chaincodes desde cero.]
