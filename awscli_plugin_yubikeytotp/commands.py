from awscli.customizations.commands import BasicCommand
import sys
from . import boto_plugin


class SessionEnv(BasicCommand):
    NAME = "session-env"
    DESCRIPTION = (
        "prints the current session's credentials in the form of "
        "environment variables.\n"
        "\n"
        "You can use the ``--profile`` argument to select a different set "
        "of credentials.\n"
        "\n"
        ".. note::\n"
        "  If you have set the environment variables in your shell, subsequent "
        "  calls to aws session-env will use those credentials. In order to use "
        "  your default profile, you have to explicitly specify it::\n"
        "\n"
        "    $(aws session-env --profile default\n"
    )
    SYNOPSIS = "aws session-env"
    EXAMPLES = (
        "Print temporary session tokens for a given profile::\n"
        "\n"
        "  $ aws session-env --profile profile_name\n"
        "  export AWS_ACCESS_KEY_ID=AKIAI44QH8DHBEXAMPLE\n"
        "  export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\n"
        "  export AWS_SESSION_TOKEN=AQoDYXdzEJr...\n"
        "  The acquired credentials will be valid for 60:00 minutes\n"
        "\n"
        "Directly set the environment variables for use in other applications::\n"
        "\n"
        "  $ $(aws session-env --profile profile_name\n"
        "  The acquired credentials will be valid for 60:00 minutes\n"
    )

    ARG_TABLE = []

    def _run_main(self, args, parsed_globals):
        credentials = self._session.get_credentials()

        frozen_credentials = credentials.get_frozen_credentials()
        print("export AWS_ACCESS_KEY_ID={}".format(frozen_credentials.access_key))
        print("export AWS_SECRET_ACCESS_KEY={}".format(frozen_credentials.secret_key))
        if frozen_credentials.token is None:
            print("unset AWS_SESSION_TOKEN")
        else:
            print("export AWS_SESSION_TOKEN={}".format(frozen_credentials.token))

        if hasattr(credentials, "_seconds_remaining"):
            seconds_to_expire = int(credentials._seconds_remaining())
            print(
                "The acquired credentials will be valid for {:.0f}:{:02.0f} minutes".format(
                    seconds_to_expire // 60, seconds_to_expire % 60
                ),
                file=sys.stderr,
            )
        return 0
