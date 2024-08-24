// const forge = require('node-forge');

// function encryptTimeWithGateGuard(gateGuardString) {
//     const publicKeyPem = `-----BEGIN PUBLIC KEY-----
//     MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlmYbt7sKhJXaktczQDA8
//     yRfGuRsj+yUNEHzuE21RuylAjI6SKilQWteysksAFDWEv/8av8U5eQGNI/nA3y1G
//     71vB/XvIpYhtgvz9elEzVx9wFKm6oOvKj7zzVqQ6aHNpG8hqW7LgVr3JDLucMFYs
//     W01rbGLgkO8xmwEuMoyok20mCfdvx5FVgov80ajh2U+DCd61RC+rGLPk0Rj/cj1T
//     Xoh4Q8ejPS8unvDI4S1px8JlyBRp9ZbAB2Mu3ci04w1pm4LnJaPxlLtStHt037ja
//     nwu7UaIwiQruQpcMnXsUz3G7fXxYobMZfqINawKozOc1t6MKcc7ENdu1w2VBr4hO
//     HQIDAQAB
//     -----END PUBLIC KEY-----
//     `;

//     const publicKey = forge.pki.publicKeyFromPem(publicKeyPem);
    
//     const currentTime = new Date().toISOString();
//     const message = `${currentTime}:${gateGuardString}`;

//     const encrypted = publicKey.encrypt(message, 'RSA-OAEP');

//     return forge.util.encode64(encrypted);
// }

// const gateGuardString = "your-gate-guard-string";
// const encryptedMessage = encryptTimeWithGateGuard(gateGuardString);
// console.log(encryptedMessage);
const fs = require('fs');
const forge = require('node-forge');

// Read the public key from a file
const publicKeyPem = fs.readFileSync('public_key.pem', 'utf8');

function encryptTimeWithGateGuard(gateGuardString) {
    const publicKey = forge.pki.publicKeyFromPem(publicKeyPem);
    
    const currentTime = new Date().toISOString();
    const message = `${currentTime}@${gateGuardString}`;

    // Encrypt with RSA-OAEP padding
    const encrypted = publicKey.encrypt(message, 'RSA-OAEP', {
        md: forge.md.sha256.create(), // Use SHA-256 for hashing
        mgf1: forge.mgf.mgf1.create(forge.md.sha256.create()) // Mask generation function
    });

    // Encode to base64
    return forge.util.encode64(encrypted);
}

const gateGuardString = "your-gate-guard-string";
const encryptedMessage = encryptTimeWithGateGuard(gateGuardString);
console.log(encryptedMessage);
