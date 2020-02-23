from botocore.exceptions import ProfileNotFound
import subprocess
import sys


class YubikeyTotpPrompter(object):
    def __init__(self, mfa_serial, original_prompter=None):
        self.mfa_serial = mfa_serial
        self._original_prompter = original_prompter

    def __call__(self, prompt):
        try:
            available_keys_result = subprocess.run(
                ["ykman", "oath", "list"], capture_output=True, check=True
            )
            available_keys = available_keys_result.stdout.decode("utf-8").split()
            available_keys.index(self.mfa_serial)

            print(
                "Generating OATH code on YubiKey. You may have to touch your YubiKey to proceed..."
            )
            ykman_result = subprocess.run(
                ["ykman", "oath", "code", "-s", self.mfa_serial], capture_output=True
            )
            print("Successfully created OATH code.")
            token = ykman_result.stdout.decode("utf-8").strip()
            return token
        except subprocess.CalledProcessError as e:
            print("No YubiKey found.", file=sys.stderr)
        except ValueError as e:
            print(
                "The requested mfa_serial has no OATH credentials stored on your YubiKey.",
                file=sys.stderr,
            )

        if self._original_prompter:
            return self._original_prompter(prompt)

        return None


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
    original_prompter = assume_role_provider._prompter
    assume_role_provider._prompter = YubikeyTotpPrompter(
        mfa_serial, original_prompter=original_prompter
    )


def awscli_initialize(cli):
    cli.register(
        "session-initialized",
        inject_yubikey_totp_prompter,
        unique_id="inject_yubikey_totp_provider",
    )
