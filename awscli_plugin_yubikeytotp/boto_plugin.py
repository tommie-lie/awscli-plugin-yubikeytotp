from . import inject_yubikey_totp_prompter
import botocore.session

old_init = botocore.session.Session.__init__


def patched_session_init(self, *args, **kwargs):
    old_init(self, *args, **kwargs)
    inject_yubikey_totp_prompter(self)


botocore.session.Session.__init__ = patched_session_init
