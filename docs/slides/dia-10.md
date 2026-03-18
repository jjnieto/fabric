# Día 10 — Criptografía en Fabric, identidades y herramientas

---

## Slide 1 — Cotilleos 🗞️

[IMAGEN: Sección de cotilleos del mundo blockchain empresarial - formato de periódico sensacionalista]

[NOTA PROFESOR: Buscar 2-3 noticias recientes sobre Hyperledger Fabric, blockchain empresarial o adopción institucional de DLT. Ejemplos: nuevas implementaciones de Fabric en producción, actualizaciones de versión, empresas que se unen a la Hyperledger Foundation, etc. Actualizar antes de cada edición del curso.]

---

## Slide 2 — Treasure Hunt: ¿Quién está detrás de Fabric? 🏴‍☠️

El primer despliegue de Hyperledger Fabric fue la versión 0.6 en 2016. Fue contribuido inicialmente por una gran empresa tecnológica.

**¿Cuál fue esa empresa?**

**Pista:** Su fundador inventó la máquina que hizo obsoletos los registros en papel de las oficinas.

**Misión (10 minutos):**
1. Investigar qué máquina hizo obsoletos los registros en papel
2. ¿Quién la inventó y en qué año?
3. ¿Qué empresa fundó esa persona?
4. ¿Sigue esa empresa contribuyendo a Fabric hoy?
5. **Bonus:** ¿Qué otra empresa contribuyó con código al proyecto original de Fabric? (pista: es japonesa)

---

## Slide 3 — Treasure Hunt: Solución

**Respuesta: IBM**

- **Herman Hollerith** inventó la **máquina tabuladora** en 1890 para el censo de Estados Unidos
- Su empresa, la Tabulating Machine Company, se fusionó con otras y en 1924 pasó a llamarse **IBM** (International Business Machines)
- IBM contribuyó el código base original de Hyperledger Fabric al proyecto Hyperledger en 2015
- La versión 0.6 (2016) era esencialmente código IBM
- **Bonus:** Digital Asset Holdings contribuyó código, y **Soramitsu** (japonesa) contribuyó Hyperledger Iroha, no Fabric directamente

[NOTA PROFESOR: Conectar con la idea de que Fabric nació en el mundo corporativo, a diferencia de Bitcoin/Ethereum que nacieron de la comunidad cypherpunk. Esto explica muchas decisiones de diseño: identidades conocidas, permisos, confidencialidad, etc.]

---

## Slide 4 — Portada sección

**Hyperledger Fabric**
De claves criptográficas a identidades

[IMAGEN: Transición visual de una clave privada abstracta a un certificado digital con nombre, organización y sello de autoridad]

---

## Slide 5 — Recapitulación: lo que ya sabemos

En los días anteriores aprendimos:
- **Criptografía asimétrica:** clave pública + clave privada
- **Firmas digitales:** demostrar autoría sin revelar la clave privada
- **Hash:** función unidireccional para integridad

En el mundo EVM (Ethereum, Sepolia):
- La **dirección** es un hash de la clave pública
- MetaMask guarda la clave privada
- La identidad es **pseudónima**: nadie sabe quién está detrás de `0x742d...`

**Pregunta:** ¿Es esto suficiente para una red empresarial?

[NOTA PROFESOR: La respuesta es no. En una red empresarial necesitas saber quién es cada participante, qué organización representa, qué permisos tiene y poder revocar su acceso si es necesario. Esto lleva directamente a los certificados X.509.]

---

## Slide 6 — De clave pública a certificado X.509

En Ethereum, tu identidad es solo tu clave pública (comprimida como dirección).

En Fabric, tu identidad es un **certificado X.509** que contiene:
- Tu **clave pública**
- Tu **nombre** (Common Name)
- Tu **organización** (Organization)
- **Quién emitió** el certificado (Issuer)
- **Fecha de expiración**
- **Firma digital** de la autoridad que lo emitió

Es como pasar de un apodo anónimo en internet a un **DNI digital** firmado por una autoridad.

[IMAGEN: Comparativa visual: a la izquierda una dirección Ethereum simple (0x742d...), a la derecha un certificado X.509 con múltiples campos etiquetados]

---

## Slide 7 — Comparativa directa: identidad EVM vs Fabric

| Aspecto | EVM (Ethereum) | Hyperledger Fabric |
|---------|---------------|-------------------|
| **Clave privada** | En MetaMask o wallet | En el directorio `keystore/` del MSP |
| **Identidad pública** | Dirección = hash de clave pública | Certificado X.509 emitido por una CA |
| **Información** | Pseudónima (solo la dirección) | Identificada (nombre, org, rol) |
| **Quién la emite** | El propio usuario la genera | Una **Certificate Authority** (CA) de confianza |
| **Revocación** | No es posible revocar una dirección | Sí, mediante CRL (Certificate Revocation List) |
| **Pertenencia a red** | Cualquiera puede participar | Solo si tu CA está reconocida en la red |
| **Roles** | No existen nativamente | Admin, peer, client, orderer |

[NOTA PROFESOR: Esta tabla es fundamental. Insistir en que la diferencia no es solo técnica sino filosófica: Ethereum asume que no necesitas saber quién es el otro; Fabric asume que es imprescindible.]

---

## Slide 8 — PKI: la infraestructura detrás de las identidades

**PKI** = Public Key Infrastructure (Infraestructura de Clave Pública)

Es el sistema completo que permite emitir, gestionar y verificar certificados digitales.

Componentes de una PKI:

1. **Certificate Authority (CA):** la entidad que emite y firma certificados
2. **Registration Authority (RA):** verifica la identidad antes de emitir un certificado (a veces integrada en la CA)
3. **Certificados digitales:** los documentos de identidad (X.509)
4. **CRL (Certificate Revocation List):** lista de certificados revocados

[IMAGEN: Diagrama de flujo: usuario solicita certificado → RA verifica identidad → CA emite certificado firmado → usuario lo presenta en la red → la red lo verifica contra la CA]

---

## Slide 9 — Fabric CA: la autoridad de certificación de Fabric

Hyperledger Fabric incluye su propia CA: **Fabric CA**

**Operaciones principales:**

| Operación | Descripción | Comando |
|-----------|-------------|---------|
| **enroll** | Obtener un certificado (usando un secreto previo) | `fabric-ca-client enroll` |
| **register** | Registrar una nueva identidad (un admin registra a un usuario) | `fabric-ca-client register` |
| **revoke** | Revocar un certificado existente | `fabric-ca-client revoke` |
| **reenroll** | Renovar un certificado antes de que expire | `fabric-ca-client reenroll` |

**Flujo típico:**
1. El **admin** de la organización hace `enroll` con las credenciales iniciales
2. El admin hace `register` para crear una nueva identidad (ej: un usuario)
3. El nuevo usuario hace `enroll` con el secreto que le dieron
4. Si el usuario se compromete, el admin hace `revoke`

[NOTA PROFESOR: Comparar con el mundo real: el admin es como el departamento de RRHH que da de alta empleados en el sistema. El enroll es como recoger tu tarjeta de empleado el primer día.]

---

## Slide 10 — MSP: Membership Service Provider

El **MSP** es el componente que define qué identidades son válidas en la red y qué permisos tienen.

Cada organización tiene su propio MSP que contiene:
- Los certificados de las CAs de confianza
- Los certificados de los administradores
- Las reglas de validación

**En la práctica, un MSP es una carpeta** con una estructura específica de directorios y archivos.

Analogía: si la CA es la oficina que emite DNIs, el MSP es la lista de invitados en la puerta del evento. Solo entras si tu DNI fue emitido por una autoridad reconocida.

[IMAGEN: Diagrama mostrando una organización con su MSP como puerta de entrada, verificando certificados contra las CAs de confianza]

---

## Slide 11 — Estructura de carpetas del MSP

```
msp/
├── cacerts/           # Certificados raíz de las CAs de confianza
│   └── ca-org1.pem
├── signcerts/         # Tu certificado de identidad
│   └── cert.pem
├── keystore/          # Tu clave privada (¡nunca compartir!)
│   └── priv_sk
├── tlscacerts/        # Certificados de CA para TLS
│   └── tlsca-org1.pem
├── admincerts/        # Certificados de los admins (deprecated en v2.x)
│   └── admin-cert.pem
├── config.yaml        # Configuración del MSP (NodeOUs)
└── intermediatecerts/  # CAs intermedias (si las hay)
```

**Importante:**
- `keystore/` contiene tu clave privada — es el equivalente a la seed phrase de MetaMask
- `signcerts/` es tu certificado público — es lo que presentas a la red
- `cacerts/` son las "autoridades de confianza" — la red verifica tu certificado contra estas

[NOTA PROFESOR: Hacer énfasis en que esta estructura se repite para cada identidad: peers, orderers, admins y usuarios. Todos tienen un MSP con la misma estructura.]

---

## Slide 12 — Portada sección

**Hyperledger Fabric**
Criptografía específica de Fabric

[IMAGEN: Candados digitales, curvas elípticas y conexiones TLS sobre un fondo de nodos de red Fabric]

---

## Slide 13 — ECDSA con curva P-256

Fabric utiliza **ECDSA** (Elliptic Curve Digital Signature Algorithm) para las firmas digitales, al igual que Ethereum.

**Pero hay una diferencia importante en la curva:**

| Aspecto | Ethereum | Fabric |
|---------|----------|--------|
| **Algoritmo** | ECDSA | ECDSA |
| **Curva** | secp256k1 | **P-256** (también llamada prime256v1) |
| **Origen de la curva** | Propuesta por Certicom, elegida por Bitcoin | Estándar NIST (gobierno de EE.UU.) |
| **Por qué se eligió** | Satoshi la eligió para Bitcoin; Ethereum la heredó | Compatible con estándares empresariales (FIPS 140-2) |
| **Seguridad** | ~128 bits | ~128 bits |

**¿Por qué P-256?**
- Es un estándar NIST, aceptado por reguladores y auditorías empresariales
- Compatible con HSM (Hardware Security Modules) corporativos
- Los módulos criptográficos de Go la soportan nativamente
- Las empresas necesitan cumplir normativas que exigen curvas NIST

[NOTA PROFESOR: secp256k1 se eligió en Bitcoin probablemente porque no era una curva NIST (desconfianza en posibles puertas traseras del gobierno). En Fabric, al ser empresarial, la compatibilidad con estándares es más importante que la desconfianza en el NIST.]

---

## Slide 14 — Mutual TLS (mTLS)

En una web normal, solo el **servidor** demuestra su identidad al cliente (TLS unidireccional):
- Tú verificas que estás hablando con `google.com` (certificado del servidor)
- Pero Google no verifica criptográficamente quién eres tú

En Fabric se usa **Mutual TLS (mTLS)**: ambas partes se autentican.

**Flujo de mTLS:**
1. El peer A presenta su certificado TLS al peer B
2. El peer B **verifica** que el certificado de A fue emitido por una CA de confianza
3. El peer B presenta su certificado TLS al peer A
4. El peer A **verifica** que el certificado de B fue emitido por una CA de confianza
5. Se establece un canal cifrado y mutuamente autenticado

**¿Por qué es necesario?**
- Los componentes de Fabric (peers, orderers) se comunican por red
- Sin mTLS, un atacante podría suplantar un peer o un orderer
- mTLS garantiza que solo componentes legítimos participan en la red

[IMAGEN: Diagrama de dos nodos intercambiando certificados antes de establecer conexión, con flechas bidireccionales y verificación en ambos lados]

---

## Slide 15 — Resumen del modelo de identidad de Fabric

[IMAGEN: Diagrama completo del flujo de identidad en Fabric: CA emite certificado → se coloca en el MSP → el peer/usuario lo presenta a la red → la red lo verifica contra el MSP del canal]

**El flujo completo:**
1. La **CA de la organización** emite un certificado X.509
2. El certificado se almacena en la carpeta **MSP** del usuario/componente
3. Cuando el usuario envía una transacción, la firma con su **clave privada** (del `keystore/`)
4. La red verifica la firma contra el **certificado** (de `signcerts/`)
5. La red verifica que el certificado fue emitido por una **CA reconocida** (en `cacerts/`)
6. Si todo es válido, la identidad es aceptada y se aplican los permisos correspondientes

---

## Slide 16 — Práctica: Explorar certificados X.509

**Objetivo:** examinar la estructura de certificados reales generados por Fabric.

**Paso 1:** Navegar a la estructura `crypto-config` generada por `cryptogen`:
```bash
cd fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/
```

**Paso 2:** Explorar el árbol de directorios:
```bash
# En Linux/Mac:
tree -L 3

# En Windows (PowerShell):
Get-ChildItem -Recurse -Depth 3 | Format-Table Name, FullName
```

**Paso 3:** Localizar el certificado de un peer:
```bash
ls peers/peer0.org1.example.com/msp/signcerts/
```

[NOTA PROFESOR: Si los alumnos aún no tienen fabric-samples descargado, se puede hacer esta práctica más adelante (día 11) o mostrar los certificados en pantalla. Lo importante es que vean la estructura real de carpetas.]

---

## Slide 17 — Práctica: Leer un certificado con OpenSSL

**Paso 4:** Abrir un certificado y leer sus campos:
```bash
openssl x509 -in peers/peer0.org1.example.com/msp/signcerts/peer0.org1.example.com-cert.pem -text -noout
```

**Campos a identificar:**
- **Issuer:** ¿quién emitió el certificado? (la CA de Org1)
- **Subject:** ¿a quién pertenece? (peer0.org1.example.com)
- **Validity:** ¿cuándo expira?
- **Public Key Algorithm:** ¿qué algoritmo usa? (ECDSA con P-256)
- **X509v3 extensions:** ¿qué restricciones tiene?

**Paso 5:** Comparar con una dirección Ethereum:
```bash
# En MetaMask, tu identidad es solo esto:
# 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18

# En Fabric, tu identidad incluye nombre, organización,
# emisor, expiración, permisos...
```

**Pregunta para los alumnos:** ¿Cuál de las dos identidades da más información? ¿Cuál ofrece más privacidad? ¿Cuál es mejor para una red empresarial?

---

## Slide 18 — Portada sección

**Hyperledger Fabric**
Herramientas del ecosistema

[IMAGEN: Caja de herramientas abierta con iconos de línea de comandos, contenedores Docker y engranajes de configuración]

---

## Slide 19 — Herramienta: `peer` CLI

El binario `peer` es la **herramienta principal** para interactuar con la red Fabric.

**Subcomandos más importantes:**

| Subcomando | Función |
|------------|---------|
| `peer channel create` | Crear un canal |
| `peer channel join` | Unir un peer a un canal |
| `peer channel list` | Listar canales a los que pertenece el peer |
| `peer channel getinfo` | Obtener información del canal (altura del ledger, etc.) |
| `peer lifecycle chaincode install` | Instalar un chaincode en el peer |
| `peer lifecycle chaincode approve` | Aprobar un chaincode para una organización |
| `peer lifecycle chaincode commit` | Hacer commit de un chaincode en el canal |
| `peer chaincode invoke` | Invocar una función del chaincode |
| `peer chaincode query` | Consultar datos (sin generar transacción) |

[NOTA PROFESOR: No pretender que memoricen todos los comandos ahora. El objetivo es que conozcan la herramienta y sepan que existe. Mañana (día 11) la usarán en práctica.]

---

## Slide 20 — Herramientas de configuración

**`configtxgen`** — Generador de configuración de canales
- Genera el bloque génesis del ordering service
- Genera las transacciones de creación de canal
- Lee su configuración de `configtx.yaml`
```bash
configtxgen -profile TwoOrgsApplicationGenesis -outputBlock genesis.block -channelID mychannel
```

**`configtxlator`** — Traductor de configuración
- Convierte entre **protobuf** (formato binario de Fabric) y **JSON** (legible)
- Esencial para modificar la configuración de un canal en producción
```bash
configtxlator proto_decode --input config_block.pb --type common.Block --output config_block.json
```

**`cryptogen`** — Generador de material criptográfico
- Genera certificados y claves para todas las organizaciones
- **Solo para desarrollo y pruebas** — en producción se usa Fabric CA
```bash
cryptogen generate --config=crypto-config.yaml
```

---

## Slide 21 — Herramientas de gestión de identidad y ordering

**`fabric-ca-client`** — Cliente de la CA de Fabric
- Registrar y enrolar identidades
- Revocar certificados
- Gestionar atributos de identidad
```bash
fabric-ca-client enroll -u https://admin:adminpw@localhost:7054
fabric-ca-client register --id.name user1 --id.secret user1pw --id.type client
```

**`fabric-ca-server`** — Servidor de la CA de Fabric
- Servidor HTTP que emite certificados X.509
- Almacena identidades en base de datos (SQLite, PostgreSQL, MySQL)
- Soporta múltiples CAs intermedias

**`osnadmin`** — Administración del ordering service
- Crear y gestionar canales en el ordering service (Fabric 2.3+)
- Reemplaza el flujo antiguo basado en el system channel
```bash
osnadmin channel join --channelID mychannel --config-block genesis.block -o localhost:7053
```

---

## Slide 22 — Fabric SDKs

Para construir **aplicaciones cliente** que interactúan con la red Fabric:

| SDK | Lenguaje | Estado |
|-----|----------|--------|
| **Fabric Gateway** (recomendado) | Go, Node.js, Java | Activo, API simplificada (Fabric 2.4+) |
| **fabric-sdk-node** | Node.js / TypeScript | Legacy, se recomienda migrar a Gateway |
| **fabric-sdk-go** | Go | Legacy |
| **fabric-sdk-java** | Java | Legacy |

**Fabric Gateway** simplifica enormemente el desarrollo:
- El SDK envía la propuesta a un solo peer (gateway peer)
- El peer se encarga de obtener los endorsements necesarios
- El SDK solo necesita saber a qué peer conectarse

[NOTA PROFESOR: Insistir en que Fabric Gateway es el camino a seguir. Los SDKs legacy requieren que la aplicación gestione manualmente el flujo de endorsement, lo cual es mucho más complejo. En este curso usaremos Fabric Gateway cuando lleguemos a programar aplicaciones cliente.]

---

## Slide 23 — Mapa completo de herramientas

[IMAGEN: Diagrama que muestra todas las herramientas de Fabric organizadas por función: configuración (configtxgen, configtxlator, cryptogen), identidad (fabric-ca-client, fabric-ca-server), operación de red (peer, orderer, osnadmin), desarrollo de aplicaciones (Fabric Gateway SDK)]

| Categoría | Herramientas | Cuándo se usan |
|-----------|-------------|----------------|
| **Configuración** | `configtxgen`, `configtxlator`, `cryptogen` | Al crear la red y canales |
| **Identidad** | `fabric-ca-client`, `fabric-ca-server` | Gestión continua de usuarios |
| **Operación** | `peer`, `orderer`, `osnadmin` | Operación diaria de la red |
| **Desarrollo** | Fabric Gateway SDK (Go/Node/Java) | Al construir aplicaciones |
| **Contenedores** | Docker, Docker Compose | Despliegue de todos los componentes |

---

## Slide 24 — Práctica: Instalar y verificar el entorno

**Objetivo:** dejar el entorno listo para las prácticas del día 11.

**Paso 1: Verificar Docker**
```bash
docker --version
docker-compose --version
docker ps    # comprobar que Docker está corriendo
```

**Paso 2: Verificar Go** (necesario para chaincodes en Go)
```bash
go version   # debe ser >= 1.21
```

**Paso 3: Descargar fabric-samples y binarios**
```bash
curl -sSLO https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/install-fabric.sh
chmod +x install-fabric.sh
./install-fabric.sh docker samples binary
```

**Paso 4: Verificar binarios de Fabric**
```bash
export PATH=$PATH:$(pwd)/fabric-samples/bin
peer version
orderer version
configtxgen -version
```

[NOTA PROFESOR: Esta práctica es CRÍTICA. Si el entorno no queda funcionando hoy, las prácticas del día 11 no se podrán hacer. Dedicar todo el tiempo necesario a resolver problemas de instalación. Problemas comunes: Docker no está corriendo, permisos en Linux, proxy corporativo bloqueando descargas, Go no instalado.]

---

## Slide 25 — Práctica: Verificación completa del entorno

**Checklist de verificación:**

| Componente | Comando | Resultado esperado |
|-----------|---------|-------------------|
| Docker | `docker ps` | Sin errores, daemon corriendo |
| Docker Compose | `docker-compose --version` | v2.x o superior |
| Go | `go version` | 1.21 o superior |
| peer | `peer version` | Muestra versión de Fabric (2.5.x) |
| orderer | `orderer version` | Muestra versión de Fabric (2.5.x) |
| configtxgen | `configtxgen -version` | Muestra versión de Fabric (2.5.x) |
| fabric-ca-client | `fabric-ca-client version` | Muestra versión de Fabric CA |
| fabric-samples | `ls fabric-samples/test-network/` | Archivos de test-network visibles |

**Si todo funciona:** prueba rápida
```bash
cd fabric-samples/test-network
./network.sh up
./network.sh down
```

[NOTA PROFESOR: Si el `./network.sh up` funciona y luego `./network.sh down` limpia correctamente, el entorno está listo para mañana. Si hay errores, resolverlos ahora.]

---

## Slide 26 — Preguntas de repaso

1. **¿Qué información contiene un certificado X.509 que NO tiene una dirección Ethereum?**

2. **¿Cuál es la diferencia entre `enroll` y `register` en Fabric CA?**

3. **¿Qué contiene la carpeta `keystore/` del MSP? ¿Por qué nunca debe compartirse?**

4. **¿Por qué Fabric usa la curva P-256 en lugar de secp256k1 como Ethereum?**

5. **¿Qué diferencia hay entre TLS normal y Mutual TLS (mTLS)?**

6. **¿Para qué sirve la CRL (Certificate Revocation List)? ¿Existe algo equivalente en Ethereum?**

7. **¿Qué herramienta usarías para crear un canal? ¿Y para instalar un chaincode?**

8. **¿Por qué `cryptogen` no se debe usar en producción?**

9. **¿Cuál es la diferencia entre `peer chaincode invoke` y `peer chaincode query`?**

10. **¿Qué ventaja ofrece Fabric Gateway SDK sobre los SDKs legacy?**

[NOTA PROFESOR: Respuestas clave:
1. Nombre, organización, emisor, fecha de expiración, permisos.
2. Register crea la identidad (nombre + secreto); enroll obtiene el certificado usando ese secreto.
3. La clave privada. Si se comparte, cualquiera puede suplantar esa identidad.
4. P-256 es estándar NIST, compatible con regulaciones y HSMs empresariales.
5. En TLS normal solo el servidor se autentica; en mTLS ambas partes se autentican mutuamente.
6. Permite revocar certificados comprometidos. En Ethereum no hay equivalente: una dirección no se puede revocar.
7. configtxgen + peer channel create para el canal; peer lifecycle chaincode install para el chaincode.
8. Genera todo el material criptográfico de golpe, sin CA real. No permite registrar/revocar identidades dinámicamente.
9. invoke genera una transacción que modifica el estado; query solo lee sin modificar.
10. Simplifica el flujo: la aplicación envía a un solo peer y él gestiona los endorsements.]

---

## Slide 27 — Preparación para mañana

**Día 11: Test Network — primera red Fabric en acción**

Mañana será un día **100% práctico**:
- Levantaremos la red de pruebas de Fabric
- Desplegaremos un chaincode
- Ejecutaremos transacciones reales
- Romperemos cosas a propósito para entender cómo funciona la red

**Requisitos imprescindibles:**
- Docker funcionando correctamente
- fabric-samples descargado
- Binarios de Fabric accesibles en el PATH

**Si tu entorno NO funciona, avisa al profesor AHORA. Mañana no habrá tiempo para solucionar problemas de instalación.**

[IMAGEN: Pantalla de terminal con una red Fabric levantada, mostrando contenedores Docker corriendo]

---

## Actividad de relleno (si sobra tiempo)

### Escape room criptográfico (30-45 min)

- El profesor prepara 5 "pruebas" que los alumnos deben resolver en orden. Cada prueba resuelta da una pista para la siguiente.
- **Prueba 1 — El certificado sospechoso:** Se da un certificado X.509 en formato PEM. Los alumnos deben usar `openssl x509 -in cert.pem -text -noout` para descubrir: ¿Quién lo emitió? ¿Para qué organización? ¿Está caducado? La respuesta (el CN del subject) es la pista para la prueba 2.
- **Prueba 2 — El MSP incompleto:** Se da una estructura de directorios MSP con un fichero que falta. Los alumnos deben identificar qué fichero falta comparando con la estructura estándar (cacerts, signcerts, keystore, tlscacerts). El nombre del fichero que falta es la pista.
- **Prueba 3 — El mensaje cifrado:** Se da un texto cifrado con AES-256 y una clave que es la combinación de las respuestas anteriores. Los alumnos descifran con: `openssl enc -aes-256-cbc -d -in mensaje.enc -out mensaje.txt -k [clave]`. El mensaje descifrado contiene una dirección (peer0.org1.example.com).
- **Prueba 4 — El configtx.yaml roto:** Se da un configtx.yaml con 3 errores intencionales. Los alumnos deben encontrarlos (ej: MSP mal referenciado, política con sintaxis incorrecta, OrdererType inexistente).
- **Prueba 5 — La frase final:** Combinando las respuestas de todas las pruebas, los alumnos forman una frase que es una cita famosa sobre la importancia de la identidad en sistemas distribuidos.

[NOTA PROFESOR: Preparar los ficheros con antelación (cert.pem, estructura MSP en un zip, mensaje.enc, configtx.yaml roto). La actividad funciona mejor en grupos de 3. Tener preparadas las soluciones por si algún grupo se atasca. La frase final puede ser algo como "In God we trust, all others must bring certificates" — adaptada al contexto de Fabric.]
