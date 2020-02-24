[![PyPI version fury.io](https://badge.fury.io/py/awscli-plugin-yubikeytotp.svg)](https://pypi.python.org/pypi/awscli-plugin-yubikeytotp/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Yubikey authentication for AWS CLI (and boto) made easy

This plugin enables aws-cli to directly talk to your [YubiKey](https://www.yubico.com/)
to acquire an OATH-TOTP code using the YubiKey's CCID application.

Currently, FIDO-U2F is unsupported on both, [botocore](https://github.com/aws/aws-cli/issues/3607)
and [aws-cli](https://github.com/aws/aws-cli/issues/3607).
Using aws-cli with roles and a regular OATH-TOTP token at least prompts you for
the TOTP code but this is quite cumbersome to use with a YubiKey.


## Installation

`awscli-plugin-yubikeytotp` can be installed from PyPI:
```
$ pip install awscli-plugin-yubikeytotp
```
It's also possible to install it just for your user in case you don't have
permission to install packages system-wide:
```
$ pip install --user awscli-plugin-yubikeytotp
```


### Configure AWS CLI
To enable the plugin, add this to your `~/.aws/config`:
```
[plugins]
yubikeytotp = awscli_plugin_yubikeytotp
```
Also make sure to have your MFA ARN configured for your profile:
```
[profile myprofile]
role_arn = arn:aws:iam::...
mfa_serial = arn:aws:iam::...
source_profile = default
```


## Usage

Just use the `aws` command with a custom role and the plugin will do the rest:
```
$ aws s3 ls --profile myprofile
Generating OATH code on YubiKey. You may have to touch your YubiKey to proceed...
Successfully created OATH code.
2013-07-11 17:08:50 mybucket
2013-07-24 14:55:44 mybucket2
```


## Acknowledgements
* Thanks to [@woowa-hsw0](https://github.com/woowa-hsw0) for this
  [inspiration for this plugin](https://gist.github.com/woowa-hsw0/caa3340e2a7b390dbde81894f73e379d)
