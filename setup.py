from setuptools import setup
from setuptools import find_packages

import helix


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="helix",
    version=helix.__version__,
    author=helix.__author__,
    author_email="helix@ll.mit.edu",
    url="https://github.com/helix-datasets/helix",
    description=helix.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    license_files=["LICENSE.txt"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=["filemagic"],
    extras_require={
        "development": [
            "black",
            "flake8",
            "pip-tools",
            "pre-commit",
            "sphinx",
            "sphinx_rtd_theme",
        ],
        "testing": ["xmlrunner", "flake8-formatter-junit-xml"],
        # Platform-specific extras.
        # It's not necessary to specify these extras when installing HELIX.
        # Because of the environment markers here make these dependency lists
        # empty on their respective platforms, pip will assume these extensions
        # have no dependencies and automatically enable them.
        "windows": ['uninstallable;platform_system!="Windows"'],
        "linux": ['uninstallable;platform_system!="Linux"'],
    },
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["helix = helix.__main__:main"],
        "helix.blueprints": [
            "static-cmake-c = helix.blueprints.cmake.static.static:StaticCMakeCBlueprint",
            "static-cmake-cpp = helix.blueprints.cmake.static.static:StaticCMakeCppBlueprint",
            "cmake-c = helix.blueprints.cmake.cmake:CMakeCBlueprint",
            "cmake-cpp = helix.blueprints.cmake.cmake:CMakeCppBlueprint",
        ],
        "helix.components": [
            "configuration-example = helix.components.examples.configuration.configuration:ConfigurationExampleComponent",
            "minimal-example = helix.components.examples.minimal.minimal:MinimalExampleComponent",
            "windows-deletefile-file-deletion = helix.components.attack.defense_evasion.file_deletion.deletefile.deletefile:AttackWindowsDeleteFileFileDeletionComponent [windows]",
            "windows-bitblt-screen-capture = helix.components.attack.collection.screen_capture.bitblt.bitblt:AttackWindowsBitBltScreenCaptureComponent [windows]",
            "windows-regqueryvalue-query-registry = helix.components.attack.discovery.query_registry.regqueryvalue.regqueryvalue:AttackWindowsRegQueryValueQueryRegistryComponent [windows]",
            "linux-unlink-file-deletion = helix.components.attack.defense_evasion.file_deletion.unlink.unlink:AttackLinuxUnlinkFileDeletionComponent [linux]",
            "linux-remove-file-deletion = helix.components.attack.defense_evasion.file_deletion.remove.remove:AttackLinuxRemoveFileDeletionComponent [linux]",
            "linux-utime-timestomp = helix.components.attack.defense_evasion.timestomp.utime.utime:AttackLinuxUtimeTimestompComponent [linux]",
            "linux-system-command-line-interface = helix.components.attack.execution.command_line_interface.system.system:AttackLinuxSystemCommandLineInterfaceComponent [linux]",
            "linux-xlib-screen-capture = helix.components.attack.collection.screen_capture.xlib.xlib:AttackLinuxXLibScreenCaptureComponent [linux]",
            "linux-libcurl-remote-file-copy = helix.components.attack.command_and_control.remote_file_copy.libcurl.libcurl:AttackLinuxLibcURLRemoteFileCopyComponent [linux]",
            "linux-zlib-compress-data-compressed = helix.components.attack.exfiltration.data_compressed.zlib.zlib:AttackLinuxZLibCompressDataCompressedComponent [linux]",
            "linux-zlib-decompress-data-compressed = helix.components.attack.exfiltration.data_compressed.zlib.zlib:AttackLinuxZLibDecompressDataCompressedComponent [linux]",
            "linux-openssl-aes-encrypt-data-encrypted = helix.components.attack.exfiltration.data_encrypted.openssl.aes.aes:AttackLinuxOpenSSLAESEncryptDataEncryptedComponent [linux]",
            "linux-openssl-aes-decrypt-data-encrypted = helix.components.attack.exfiltration.data_encrypted.openssl.aes.aes:AttackLinuxOpenSSLAESDecryptDataEncryptedComponent [linux]",
        ],
        "helix.transforms": [
            "replace-example = helix.transforms.examples.replace.replace:ReplaceExampleTransform",
            "strip = helix.transforms.strip.strip:StripTransform [linux]",
            "upx = helix.transforms.upx.upx:UPXTransform",
            "mpress = helix.transforms.mpress.mpress:MPRESSTransform [windows]",
        ],
        "helix.tests": [
            "minimal-example = helix.components.examples.minimal.minimal:MinimalExampleComponentTests [testing]",
            "replace-example = helix.transforms.examples.replace.replace:ReplaceExampleTransformTests [testing]",
            "upx = helix.transforms.upx.tests:UPXTests [testing]",
        ],
    },
)
