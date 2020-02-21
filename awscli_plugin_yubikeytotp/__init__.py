from botocore.exceptions import ProfileNotFound
import getpass


def yubikey_totp_prompter(prompt):
    return getpass.getpass(prompt)


def inject_yubikey_totp_prompter(session, **kwargs):
    try:
        providers = session.get_component("credential_provider")
    except ProfileNotFound:
        return
    assume_role_provider = providers.get_provider("assume-role")
    assume_role_provider._prompter = yubikey_totp_prompter


def awscli_initialize(cli):
    cli.register(
        "session-initialized",
        inject_yubikey_totp_prompter,
        unique_id="inject_yubikey_totp_provider",
    )
