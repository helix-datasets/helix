from ..... import utils
from ....... import exceptions
from ....... import utils as helix_utils


class AESConfigurationValidationMixin(object):
    def validate_configuration(self):
        if len(self.configuration["key"]) != 32:
            raise exceptions.ConfigurationError(
                "{}: key must be exactly 32 characters (256 bits)".format(self.name)
            )

        if len(self.configuration["iv"]) != 16:
            raise exceptions.ConfigurationError(
                "{}: iv must be exactly 16 characters (128 bits)".format(self.name)
            )


class AttackLinuxOpenSSLAESEncryptDataEncryptedComponent(
    AESConfigurationValidationMixin, utils.SimpleTemplatedComponent
):
    """Linux AES file encryption with OpenSSL.

    Note:
        This component requires openssl-dev to be installed.
    """

    name = "linux-openssl-aes-encrypt-data-encrypted"
    verbose_name = "Linux OpenSSL AES Encrypt Data Encrypted"
    description = "Linux AES file encryption with OpenSSL"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "exfiltration"),
        ("technique", "data-encrypted"),
        ("id", "T1022"),
        ("name", "linux-openssl-aes-encrypt"),
    )

    options = {
        "input": {},
        "output": {},
        "key": {},
        "iv": {"default": "0123456789012345"},
    }

    dependencies = [helix_utils.LinuxAPTDependency("libssl-dev")]

    libraries = ["crypto"]

    source = "linux-encrypt-openssl-aes.cpp"
    function = "linux_encrypt_openssl_aes"


class AttackLinuxOpenSSLAESDecryptDataEncryptedComponent(
    AESConfigurationValidationMixin, utils.SimpleTemplatedComponent
):
    """Linux AES file decryption with OpenSSL.

    Note:
        This component requires openssl-dev to be installed.
    """

    name = "linux-openssl-aes-decrypt-data-encrypted"
    verbose_name = "Linux OpenSSL AES Decrypt Data Encrypted"
    description = "Linux AES file decryption with OpenSSL"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "exfiltration"),
        ("technique", "data-encrypted"),
        ("id", "T1022"),
        ("name", "linux-openssl-aes-decrypt"),
    )

    options = {
        "input": {},
        "output": {},
        "key": {},
        "iv": {"default": "0123456789012345"},
    }

    dependencies = [helix_utils.LinuxAPTDependency("libssl-dev")]

    libraries = ["crypto"]

    source = "linux-decrypt-openssl-aes.cpp"
    function = "linux_decrypt_openssl_aes"
