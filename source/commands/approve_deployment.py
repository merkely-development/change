from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload
from cdb.git import repo_at, list_commits_between


class ApproveDeployment(Command):

    def summary(self, _ci):
        return "Logs an approval."

    def volume_mounts(self, ci):
        mounts = ["${PWD}:/src"]
        if ci != 'bitbucket':
            mounts.append("/var/run/docker.sock:/var/run/docker.sock")
        return mounts

    def __call__(self):
        commit_list = list_commits_between(repo_at(self.src_repo_root.value),
                                           self.newest_src_commitish.value,
                                           self.oldest_src_commitish.value)
        payload = {
            "artifact_sha256": self.fingerprint.sha,
            "description": self.description.value,
            "src_commit_list": commit_list,
            "user_data": self.user_data.value,
            "approvals": [
                {
                    "state": 'APPROVED',
                    "comment": self.description.value,
                    "approved_by": "External",
                    "approval_url": "undefined"
                }
            ]
        }
        url = ApiSchema.url_for_approvals(self.host.value, self.merkelypipe)
        http_post_payload(url, payload, self.api_token.value)
        return 'Posting', url, payload

    @property
    def description(self):
        return DescriptionEnvVar(self.env)

    @property
    def oldest_src_commitish(self):
        return OldestSrcCommitishEnvVar(self.env)

    @property
    def newest_src_commitish(self):
        return NewestSrcCommitishEnvVar(self.env)

    @property
    def src_repo_root(self):
        return SrcRepoRootEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'oldest_src_commitish',
            'newest_src_commitish',
            'description',
            'src_repo_root',
            'user_data',
            'owner',
            'pipeline',
            'api_token',
            'host',
        ]


class DescriptionEnvVar(RequiredEnvVar):

    def __init__(self, env):
        notes = f"A description for the approval."
        super().__init__(env, "MERKELY_DESCRIPTION", notes)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"Approval created by ${{ github.actor }} on github"'
        if ci_name == 'bitbucket':
            return True, '"Production release requested"'
        return False, ""
