"""
# Trying to use reflection but my Python fu is not
# strong enough yet...

from commands import LogEvidence, External
from env_vars import RequiredEnvVar

from collections import namedtuple


def make_env_var_marker():
    def marker(func):
        func.is_env_var = True
        return func
    return marker


class Example:
    env_var = make_env_var_marker()

    @property
    def env_vars(self):
        names = [
            'api_token',
            'host',
        ]
        evs = [getattr(self, name) for name in names]
        return namedtuple('EnvVars', tuple(names))(*evs)

    @property
    def X_env_vars(self):
        names = []
        evs = []
        for name,maybe in Example.__dict__.items():
            # print(f"Looking at {item!r} {type(item)}")
            if hasattr(maybe, 'is_env_var'):
                names.append(name)
                evs.append(maybe())
        return namedtuple('EnvVars', tuple(names))(*evs)

    @property
    @env_var
    def api_token(self):
        ev = {"MERKELY_API_TOKEN": "3455643212456"}
        return RequiredEnvVar(ev, "MERKELY_API_TOKEN", "notes")

    @property
    @env_var
    def host(self):
        ev = {"MERKELY_HOST": "https://tests.merkely.com"}
        return RequiredEnvVar(ev, "MERKELY_HOST", "notes")


def X_test_env_vars_using_env_var_decorator():
    eg = Example()
    assert len(eg.env_vars) == 2
    assert eg.env_vars.api_token.name == "MERKELY_API_TOKEN"
    assert eg.env_vars.api_token.value == "3455643212456"
    assert eg.env_vars.host.name == "MERKELY_HOST"
    assert eg.env_vars.host.value == "https://tests.merkely.com"


def X_test_env_vars():
    domain = "app.merkely.com"
    build_url = "https://gitlab/build/1956"
    protocol = "docker://"
    image_name = "acme/widget:4.67"
    api_token = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
    env = {
        "MERKELY_API_TOKEN": api_token,
        "MERKELY_CI_BUILD_URL": build_url,
        "MERKELY_COMMAND": "log_evidence",
        "MERKELY_DESCRIPTION": "branch coverage",
        "MERKELY_EVIDENCE_TYPE": "unit_test",
        "MERKELY_FINGERPRINT": f"{protocol}/{image_name}",
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_IS_COMPLIANT": "TRUE",
    }
    command = LogEvidence(External(env=env))
    env_vars = command.merkely_env_vars

    assert env_vars.api_token.value == api_token
    assert env_vars.ci_build_url.value == build_url
    assert env_vars.description.value == "branch coverage"
    assert env_vars.evidence_type.value == "unit_test"
    assert env_vars.fingerprint.value == f"{protocol}/{image_name}"
    assert env_vars.host.value == f"https://{domain}"
    assert env_vars.is_compliant.value == 'TRUE'
"""
