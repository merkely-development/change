from cdb.put_artifact import put_artifact

from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_all_env_vars_defined(capsys):
    env = {
        "CDB_HOST": "http://test.compliancedb.com",
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "tests/data/coverage.txt",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": "http://github/me/project/commit/abc50c8a53f79974d615df335669b59fb56a4ed3",
        "CDB_ARTIFACT_GIT_COMMIT": "abc50c8a53f79974d615df335669b59fb56a4ed3",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1456",
        "CDB_BUILD_NUMBER": "349"
    }
    set_env_vars = {'CDB_ARTIFACT_SHA': 'ccee89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc'}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_CDB_ARTIFACT_FILENAME_is_missing(capsys):
    set_env_vars = {}
    with AutoEnvVars(CDB_DRY_RUN, set_env_vars):
        put_artifact("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_CDB_ARTIFACT_SHA_is_UNDEFINED(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests/data/coverage.txt",
        "CDB_ARTIFACT_SHA": "UNDEFINED"
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_CDB_ARTIFACT_SHA_is_not_defined(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests/data/coverage.txt",
    }
    set_env_vars = {
        "CDB_ARTIFACT_SHA": "ccee89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    }
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_CDB_ARTIFACT_SHA_is_defined(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests/data/coverage.txt",
        "CDB_ARTIFACT_SHA": "ccee89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])
