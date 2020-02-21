from botocore.exceptions import ProfileNotFound
import subprocess
import sys


class YubikeyTotpPrompter(object):
    def __init__(self, mfa_serial):
        self.mfa_serial = mfa_serial

    def __call__(self, prompt):
        available_keys_result = subprocess.run(
            ["ykman", "oath", "list"], capture_output=True
        )
        if available_keys_result.returncode != 0:
            print("No YubiKey found.", file=sys.stderr)
            return

        available_keys = available_keys_result.stdout.decode("utf-8").split()
        if not self.mfa_serial in available_keys:
            print(
                "The requested mfa_serial has no OATH credentials stored on your YubiKey.",
                file=sys.stderr,
            )
            return

        print(
            "Generating OATH code on YubiKey. You may have to touch your YubiKey to proceed..."
        )
        ykman_result = subprocess.run(
            ["ykman", "oath", "code", "-s", self.mfa_serial], capture_output=True
        )
        token = ykman_result.stdout.decode("utf-8").strip()
        return token


def inject_yubikey_totp_prompter(session, **kwargs):
    try:
        providers = session.get_component("credential_provider")
    except ProfileNotFound:
        return

    config = session.get_scoped_config()
    mfa_serial = config.get("mfa_serial")
    if mfa_serial is None:
        # no MFA, so don't interfere with regular flow
        return

    assume_role_provider = providers.get_provider("assume-role")
    assume_role_provider._prompter = YubikeyTotpPrompter(mfa_serial)


def awscli_initialize(cli):
    cli.register(
        "session-initialized",
        inject_yubikey_totp_prompter,
        unique_id="inject_yubikey_totp_provider",
    )
