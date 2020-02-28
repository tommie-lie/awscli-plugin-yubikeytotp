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

---
**NOTE**

To AWS, the M in MFA [still stands for the number 2](https://forums.aws.amazon.com/thread.jspa?threadID=137055). Hence, if you want to log in to the AWS console with OATH-TOTP
enabled, you will have to use `ykman oath code` to generate a key and enter it
manually to log in, just like with Google Authenticator or Yubikey Authenticator
smartphone apps.

If you want to use U2F MFA authentication for login while still being able to
use your YubiKey for command line, you should create multiple IAM users. Use
one user with U2F MFA to log in to the AWS console and disable access keys.
Use the other use with Virtual MFA device and disable console login.
Only ever use one user in the console and the other on your command line.

---


## Tutorial

### Prerequisites

You obviously have to have a YubiKey. A Yubico Security Key (the blue ones)
are not supported as they lack the OATH application.

To setup your YubiKey, you also have to have [yubikey-manager](https://developers.yubico.com/yubikey-manager/) (or `ykman`) installed.
You can use it to verify that OATH is enabled for your YubiKey:
```
$ ykman info
Device type: YubiKey 5 NFC
Serial number: 00000000
Firmware version: 5.2.4
Form factor: Keychain (USB-A)
Enabled USB interfaces: OTP+FIDO+CCID
NFC interface is enabled.

Applications    USB     NFC    
OTP             Enabled Enabled
FIDO U2F        Enabled Enabled
OpenPGP         Enabled Enabled
PIV             Enabled Enabled
OATH            Enabled Enabled
FIDO2           Enabled Enabled
```

### Setup MFA in AWS

1. Log-in to your AWS account/user and navigate to your *My Security Credentials*
page.
2. Take not of your *AWS account ID* at the top.
2. Under *Multi-factor authentivation (MFA)*, click `Manage MFA device` and add
a *Virtual MFA device*.
3. Instead of showing the QR code, click on `Show secret key` and copy the key.
4. On a command line, run
   ```
   $ ykman oath add -t arn:aws:iam::${ACCOUNT_ID}:mfa/${IAM_USERNAME} ${MFA_SECRET}
   ```
   The strange string `arn:aws:iam::${ACCOUNT_ID}:mfa/${IAM_USERNAME}` will
   be your user's MFA serial after you have set up everything. The AWS console
   will not tell you the MFA serial in advance, but by replacing the account id
   and IAM username, you can build it on your own, e.g.:
   ```
   $ ykman oath add -t arn:aws:iam::123456789012:mfa/tommie-lie ABCD1234...
   ```
   
   The above command requires you to touch your YubiKey to generate
   authentication codes. You can ommit `-t` if you don't want to touch your key
   every time you authenticate.
5. Now you have to enter two **consecutive** MFA codes into the AWS website
   to assign your key to your AWS login. Just run
   `ykman oath code arn:aws:iam::${ACCOUNT_ID}:mfa/${IAM_USERNAME}`
   to get an authentication code.
   The codes are re-generated every 30 seconds, so you have to run this command
   twice with about 30 seconds in between to get two distinct codes.
   
   Enter the two codes in the AWS form and click `Assign MFA`
6. You're done!


### Setup AWS CLI

1. AWS CLI only asks for MFA if you change roles, but role-based access
   management is a good practice for AWS security anyway, so we'll assume you
   already have a role and a profile configured in your AWS CLI config file.
2. Install `awscli-plugin-yubikeytotp`, see [installation section](#installation).
3. Edit your AWS CLI config file (`~/.aws/config`) and add the MFA serial to
   the profile you want to use MFA authentication with:
   <pre><code>
   [profile yubikey]
   role_arn = arn:aws:iam::123456789012:role/yubikey-role
   <b>mfa_serial = arn:aws:iam::123456789012:mfa/tommie-lie</b>
   source_profile = default
   </code></pre>
4. Enable the plugin by appending the following section to your AWS CLI config file:
   ```
   [plugins]
   yubikeytotp = awscli_plugin_yubikeytotp
   ```
5. That's it, you're ready to use AWS CLI with your YubiKey now!


### Test your setup

If you need authentication by switching to another IAM role to access certain
resources, you will normally get a permission denied error:
```
$ aws s3 ls

An error occurred (AccessDenied) when calling the ListBuckets operation: Access Denied
```
If you switch profiles, however, AWS CLI will automatically ask for an MFA code:
```
$ aws s3 ls --profile yubikey
Generating OATH code on YubiKey. You may have to touch your YubiKey to proceed...
Successfully created OATH code.
2013-07-11 17:08:50 mybucket
2013-07-24 14:55:44 mybucket2
```


## Acknowledgements
* Thanks to [@woowa-hsw0](https://github.com/woowa-hsw0) for this
  [inspiration for this plugin](https://gist.github.com/woowa-hsw0/caa3340e2a7b390dbde81894f73e379d)
