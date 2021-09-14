#include <stdio.h>
#include <string.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

#define CHUNK 1024

int ${linux_encrypt_openssl_aes}(int argv, char* argc[]){
    // https://wiki.openssl.org/index.php/EVP_Symmetric_Encryption_and_Decryption
    int status;
    int len;
    size_t read;

    unsigned char plaintext[CHUNK];
    unsigned char ciphertext[CHUNK];

    FILE *input = fopen(${input}, "r");

    if(input == NULL)
        return 1;

    FILE *output = fopen(${output}, "wb");

    if(output == NULL)
        return 1;

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    if(ctx == NULL)
        return 1;

    status = EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, (const unsigned char*)${key}, (const unsigned char*)${iv});

    if(status != 1)
        return 1;

    read = fread(plaintext, 1, CHUNK, input);
    while(read > 0) {
        status = EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, read);

        if(status != 1)
            return 1;
        
        fwrite(ciphertext, 1, len, output);

        read = fread(plaintext, 1, CHUNK, input);
    }

    status = EVP_EncryptFinal_ex(ctx, ciphertext, &len);

    if(status != 1)
        return 1;

    fwrite(ciphertext, 1, len, output);

    EVP_CIPHER_CTX_free(ctx);

    fflush(output);

    fclose(input);
    fclose(output);

    return 0;
}
