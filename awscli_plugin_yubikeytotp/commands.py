from awscli.customizations.commands import BasicCommand

from . import boto_plugin


class YkLogin(BasicCommand):
    NAME = "yklogin"
    DESCRIPTION = (
        "is a plugin that manages retrieving and rotating"
        " Amazon STS keys using the Shibboleth IdP and Duo"
        " for authentication."
    )
    SYNOPSIS = "aws yklogin [<Arg> ...]"

    ARG_TABLE = []

    def _run_main(self, args, parsed_globals):
        credentials = self._session.get_credentials()

        frozen_credentials = credentials.get_frozen_credentials()
        print("export AWS_ACCESS_KEY_ID={}".format(frozen_credentials.access_key))
        print("export AWS_SECRET_ACCESS_KEY={}".format(frozen_credentials.secret_key))
        print("export AWS_SESSION_TOKEN={}".format(frozen_credentials.token))

        seconds_to_expire = int(credentials._seconds_remaining())
        print(
            "The acquired credentials will be valid for {:.0f}:{:02.0f} minutes".format(
                seconds_to_expire / 60, seconds_to_expire % 60
            )
        )
        return 0
