from commands import run, External
from tests.utils import *

DOMAIN = "app.merkely.com"
OWNER = "acme"
PIPELINE = "lib-controls-test-pipeline"

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_docker_image():
    image_name = "acme/runner:4.56"
    sha256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"

    expected_method = "POST"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/approvals/"
    expected_payload = {
        "artifact_sha256": sha256,
        "description": "The approval request description here",
        'user_data': {},
        "src_commit_list": [
            "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
            "e0ad84e1a2464a9486e777c1ecde162edff930a9"
        ],
        "approvals": []
    }

    env = dry_run(request_approval_env())
    with ScopedDirCopier("/test_src", "/src"):
        with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def request_approval_env():
    protocol = "docker://"
    image_name = "acme/runner:4.56"
    return {
        "MERKELY_COMMAND": "request_approval",
        "MERKELY_OWNER": OWNER,
        "MERKELY_PIPELINE": PIPELINE,
        "MERKELY_FINGERPRINT": f"{protocol}{image_name}",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_OLDEST_SRC_COMMITISH": "production",
        "MERKELY_NEWEST_SRC_COMMITISH": "master",
        "MERKELY_DESCRIPTION": "The approval request description here",
    }



