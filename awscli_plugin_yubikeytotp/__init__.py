from .prompter import inject_yubikey_totp_prompter
from .commands import SessionEnv


def awscli_initialize(cli):
    cli.register(
        "session-initialized",
        inject_yubikey_totp_prompter,
        unique_id="inject_yubikey_totp_provider",
    )
    cli.register("building-command-table.main", awscli_register_commands)


def awscli_register_commands(command_table, session, **kwargs):
    command_table["session-env"] = SessionEnv(session)
