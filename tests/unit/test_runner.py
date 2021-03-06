from commands import run, External
from errors import ChangeError
from tests.utils import *
from pytest import raises

IMAGE_NAME = "acme/road-runner:4.56"
SHA256 = "efcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
PROTOCOL = "docker://"
BUILD_URL = "https://gitlab/build/1456"
DOMAIN = "app.merkely.com"


def test_raises_when_merkely_command_not_set():
    env = dry_run(core_env_vars('log_artifact'))
    env.pop("MERKELY_COMMAND")

    with raises(ChangeError):
        run(External(env=env))


def test_raises_when_merkely_command_is_empty_string():
    env = dry_run(core_env_vars('log_artifact'))
    env["MERKELY_COMMAND"] = ""

    with raises(ChangeError):
        run(External(env=env))


def test_raises_when_merkely_command_is_unknown():
    env = dry_run(core_env_vars('log_artifact'))
    env["MERKELY_COMMAND"] = "wibble"

    with raises(ChangeError):
        run(External(env=env))


def test_merkely_command_when_method_is_get(mocker):
    # ControlDeployment command is used for this test
    env = dry_run(control_deployment_env())
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        method, url, payload = run(external)

    assert method == 'GET'
    assert len(url) > 0
    assert payload != []


def test_merkely_command_when_method_is_post():
    # LogDeployment command is used for this test
    env = dry_run(log_deployment_env())
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        method, url, payload = run(external)

    assert method == 'POST'
    assert len(url) > 0
    assert payload != []


def test_merkely_command_when_method_is_put():
    # LogEvidence command is used for this test
    env = dry_run(log_evidence_env())
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        method, url, payload = run(external)

    assert method == 'PUT'
    assert len(url) > 0
    assert payload != []


def control_deployment_env():
    ev = {"MERKELY_FINGERPRINT": f"{PROTOCOL}{IMAGE_NAME}"}
    return {**core_env_vars("control_deployment"), **ev}


def log_deployment_env():
    ev = {
        "MERKELY_CI_BUILD_URL": BUILD_URL,
        "MERKELY_ENVIRONMENT": "production",
        "MERKELY_DESCRIPTION": "some description",
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_USER_DATA": "/app/tests/data/user_data.json",
        "MERKELY_FINGERPRINT": f"{PROTOCOL}{IMAGE_NAME}",
    }
    # MERKELY_OWNER and MERKELY_PIPELINE set in core_env_vars
    return {**core_env_vars("log_deployment"), **ev}


def log_evidence_env():
    protocol = "docker://"
    return {
        "MERKELY_COMMAND": "log_evidence",
        "MERKELY_OWNER": "acme",
        "MERKELY_PIPELINE": "lib-controls-test-pipeline",
        "MERKELY_FINGERPRINT": f"{protocol}{IMAGE_NAME}",
        "MERKELY_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_CI_BUILD_URL": BUILD_URL,
        "MERKELY_IS_COMPLIANT": "TRUE",
        "MERKELY_EVIDENCE_TYPE": "unit_test",
        "MERKELY_DESCRIPTION": "branch coverage"
    }
