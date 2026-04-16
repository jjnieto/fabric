'use strict';

const { Gateway, Wallets } = require('fabric-network');
const path = require('path');
const fs = require('fs');

/**
 * Conecta al Gateway de Fabric y devuelve el contrato.
 * @param {string} org - 'hotel' o 'cafeteria'
 * @returns {Object} { gateway, contract, network }
 */
async function connectToFabric(org) {
    const config = {
        hotel: {
            msp: 'HotelMSP',
            domain: 'hotel.fidelitychain.com',
            peerPort: '7051',
        },
        cafeteria: {
            msp: 'CafeteriaMSP',
            domain: 'cafeteria.fidelitychain.com',
            peerPort: '9051',
        },
    };

    const orgConfig = config[org];
    if (!orgConfig) throw new Error(`Org desconocida: ${org}`);

    const networkPath = path.resolve(__dirname, '..', '..', 'network');
    const cryptoPath = path.join(networkPath, 'crypto-config', 'peerOrganizations',
        orgConfig.domain);

    // Leer certificado del admin
    const certPath = path.join(cryptoPath, 'users', `Admin@${orgConfig.domain}`,
        'msp', 'signcerts');
    const certFile = fs.readdirSync(certPath)[0];
    const certificate = fs.readFileSync(path.join(certPath, certFile), 'utf8');

    // Leer clave privada del admin
    const keyPath = path.join(cryptoPath, 'users', `Admin@${orgConfig.domain}`,
        'msp', 'keystore');
    const keyFile = fs.readdirSync(keyPath)[0];
    const privateKey = fs.readFileSync(path.join(keyPath, keyFile), 'utf8');

    // Crear wallet en memoria con la identidad del admin
    const wallet = await Wallets.newInMemoryWallet();
    const identity = {
        credentials: { certificate, privateKey },
        mspId: orgConfig.msp,
        type: 'X.509',
    };
    await wallet.put('admin', identity);

    // Leer certificado TLS del peer
    const tlsCertPath = path.join(cryptoPath, 'peers',
        `peer0.${orgConfig.domain}`, 'tls', 'ca.crt');
    const tlsCert = fs.readFileSync(tlsCertPath, 'utf8');

    // Leer certificado TLS del orderer
    const ordererTlsCert = fs.readFileSync(path.join(networkPath, 'crypto-config',
        'ordererOrganizations', 'fidelitychain.com', 'orderers',
        'orderer.fidelitychain.com', 'tls', 'ca.crt'), 'utf8');

    // Connection profile programatico
    const ccp = {
        name: `fidelitychain-${org}`,
        version: '1.0.0',
        channels: {
            'fidelity-channel': {
                orderers: ['orderer.fidelitychain.com'],
                peers: { [`peer0.${orgConfig.domain}`]: {} },
            },
        },
        organizations: {
            [orgConfig.msp]: {
                mspid: orgConfig.msp,
                peers: [`peer0.${orgConfig.domain}`],
            },
        },
        orderers: {
            'orderer.fidelitychain.com': {
                url: 'grpcs://localhost:7050',
                tlsCACerts: { pem: ordererTlsCert },
                grpcOptions: {
                    'ssl-target-name-override': 'orderer.fidelitychain.com',
                },
            },
        },
        peers: {
            [`peer0.${orgConfig.domain}`]: {
                url: `grpcs://localhost:${orgConfig.peerPort}`,
                tlsCACerts: { pem: tlsCert },
                grpcOptions: {
                    'ssl-target-name-override': `peer0.${orgConfig.domain}`,
                },
            },
        },
    };

    // Conectar al Gateway
    const gateway = new Gateway();
    await gateway.connect(ccp, {
        wallet,
        identity: 'admin',
        discovery: { enabled: true, asLocalhost: true },
    });

    const network = await gateway.getNetwork('fidelity-channel');
    const contract = network.getContract('fidelitypoints');

    return { gateway, contract, network };
}

module.exports = { connectToFabric };
