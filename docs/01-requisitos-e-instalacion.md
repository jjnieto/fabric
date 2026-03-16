# 01 - Requisitos previos e instalación de Hyperledger Fabric

## Sistemas operativos soportados

- **Linux** (Ubuntu/Debian recomendado)
- **macOS**
- **Windows** (mediante WSL2 — Windows Subsystem for Linux 2)

> **Nota para Windows:** Todo el desarrollo en Fabric se realiza dentro de WSL2.
> No se ejecutan binarios de Fabric nativamente en Windows.

---

## 1. Habilitar WSL2 (solo Windows)

### 1.1 Instalar WSL2

Abrir PowerShell como administrador:

```powershell
wsl --install
```

Esto instala WSL2 con Ubuntu por defecto. Si ya tienes WSL1, actualiza:

```powershell
wsl --set-default-version 2
```

Reinicia el equipo si se te solicita.

### 1.2 Verificar la instalación

```powershell
wsl --list --verbose
```

Debes ver tu distribución con `VERSION 2`.

### 1.3 Acceder a WSL

```powershell
wsl
```

**A partir de aquí, todos los comandos se ejecutan dentro de la terminal de Linux (WSL2 o nativa).**

---

## 2. Instalar prerequisitos del sistema

### Ubuntu / Debian (o WSL2 con Ubuntu)

```bash
sudo apt-get update
sudo apt-get install -y git curl wget jq tree
```

### macOS

```bash
brew install git curl wget jq tree
```

### Verificar versiones

```bash
git --version
curl --version
jq --version
```

---

## 3. Instalar Docker

Docker es **imprescindible**. Fabric ejecuta todos sus componentes (peers, orderers, CAs) como contenedores Docker.

### Ubuntu / WSL2

```bash
# Eliminar versiones antiguas
sudo apt-get remove -y docker docker-engine docker.io containerd runc

# Instalar dependencias
sudo apt-get update
sudo apt-get install -y ca-certificates gnupg lsb-release

# Añadir clave GPG oficial de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Añadir repositorio
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### macOS

Instalar Docker Desktop desde [docker.com](https://www.docker.com/products/docker-desktop/) o:

```bash
brew install --cask docker
```

### Configurar Docker sin sudo (Linux/WSL2)

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Verificar Docker

```bash
docker --version
docker compose version
docker run hello-world
```

---

## 4. Instalar Go (opcional pero recomendado)

Necesario si vas a desarrollar chaincodes en Go (el lenguaje más usado en Fabric).

```bash
# Descargar Go (verificar última versión en https://go.dev/dl/)
wget https://go.dev/dl/go1.22.5.linux-amd64.tar.gz

# Instalar
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.22.5.linux-amd64.tar.gz

# Configurar PATH (añadir al final de ~/.bashrc o ~/.zshrc)
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc
```

### Verificar

```bash
go version
```

---

## 5. Instalar Node.js (opcional)

Necesario si vas a desarrollar chaincodes en JavaScript/TypeScript o usar el SDK de Fabric para aplicaciones cliente.

```bash
# Instalar nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

# Instalar Node.js LTS
nvm install --lts
nvm use --lts
```

### Verificar

```bash
node --version
npm --version
```

---

## 6. Descargar Hyperledger Fabric

### 6.1 Crear directorio de trabajo

```bash
mkdir -p $HOME/fabric
cd $HOME/fabric
```

### 6.2 Descargar el script de instalación

```bash
curl -sSLO https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/install-fabric.sh
chmod +x install-fabric.sh
```

### 6.3 Ver opciones disponibles

```bash
./install-fabric.sh -h
```

### 6.4 Instalar todo: imágenes Docker + binarios + samples

```bash
./install-fabric.sh docker samples binary
```

Esto descarga:

| Componente | Descripción |
|---|---|
| **fabric-samples/** | Repositorio con ejemplos y la test-network |
| **bin/** | Binarios CLI: `peer`, `orderer`, `configtxgen`, `configtxlator`, `osnadmin`, `cryptogen`, `fabric-ca-client`, `fabric-ca-server` |
| **config/** | Archivos de configuración base: `core.yaml`, `orderer.yaml`, `configtx.yaml` |
| **Imágenes Docker** | `hyperledger/fabric-peer`, `fabric-orderer`, `fabric-ca`, `fabric-tools`, `fabric-ccenv`, `fabric-baseos` |

### 6.5 Especificar versiones (opcional)

```bash
# Versión específica de Fabric y CA
./install-fabric.sh -f 2.5.15 -c 1.5.17 docker samples binary
```

### 6.6 Configurar PATH de los binarios

```bash
# Añadir al final de ~/.bashrc o ~/.zshrc
echo 'export PATH=$HOME/fabric/fabric-samples/bin:$PATH' >> ~/.bashrc
echo 'export FABRIC_CFG_PATH=$HOME/fabric/fabric-samples/config' >> ~/.bashrc
source ~/.bashrc
```

### 6.7 Verificar la instalación

```bash
peer version
orderer version
configtxgen -version
fabric-ca-client version
```

---

## 7. Verificar imágenes Docker descargadas

```bash
docker images | grep hyperledger
```

Deberías ver algo similar a:

```
hyperledger/fabric-tools      2.5
hyperledger/fabric-peer        2.5
hyperledger/fabric-orderer     2.5
hyperledger/fabric-ccenv       2.5
hyperledger/fabric-baseos      2.5
hyperledger/fabric-ca          1.5
```

---

## 8. Resumen de lo instalado

```
$HOME/fabric/
├── install-fabric.sh          # Script de instalación
└── fabric-samples/            # Repositorio de ejemplos
    ├── bin/                   # Binarios de Fabric
    │   ├── peer
    │   ├── orderer
    │   ├── configtxgen
    │   ├── configtxlator
    │   ├── osnadmin
    │   ├── cryptogen
    │   ├── fabric-ca-client
    │   └── fabric-ca-server
    ├── config/                # Configuración base
    │   ├── configtx.yaml
    │   ├── core.yaml
    │   └── orderer.yaml
    ├── test-network/          # Red de pruebas
    ├── asset-transfer-basic/  # Chaincode de ejemplo
    └── ...                    # Más ejemplos
```

---

## Checklist final

- [ ] WSL2 funcionando (solo Windows)
- [ ] Git, curl, jq instalados
- [ ] Docker funcionando sin sudo
- [ ] Docker Compose disponible
- [ ] Go instalado (si vas a escribir chaincodes en Go)
- [ ] Node.js instalado (si vas a usar SDK o chaincodes JS/TS)
- [ ] Binarios de Fabric en el PATH (`peer version` funciona)
- [ ] Imágenes Docker de Fabric descargadas
- [ ] `fabric-samples` clonado

---

**Siguiente:** [02 - Test Network: tu primera red Fabric](02-test-network.md)
