from botocore.exceptions import ProfileNotFound
import getpass


class YubikeyTotpPrompter(object):
    def __init__(self, mfa_serial):
        self.mfa_serial = mfa_serial

    def __call__(self, prompt):
        return getpass.getpass(prompt)


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
