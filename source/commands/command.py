from abc import ABC
from collections import namedtuple
from env_vars import *
from errors import ChangeError
import re
import copy


class Command(ABC):
    """
    Abstract Base Class for all merkely/change commands.
    """
    def __init__(self, external):
        self._external = external

    # - - - - - - - - - - - - - - - - - - - - -
    # Builder methods

    @staticmethod
    def names():
        return copy.deepcopy(Command.__names)

    @staticmethod
    def named(string):
        name = "".join(list(s.capitalize() for s in string.split('_')))
        try:
            return Command.__classes[name]
        except KeyError:
            raise ChangeError(f"Unknown command: {string}")

    def __init_subclass__(cls):
        super().__init_subclass__()
        Command.__classes[cls.__name__] = cls
        parts = re.findall('[A-Z][^A-Z]*', cls.__name__)
        Command.__names.append("_".join(part.lower() for part in parts))

    __classes = {}
    __names = []

    # - - - - - - - - - - - - - - - - - - - - -
    # os env-vars

    @property
    def env(self):
        return self._external.env

    # - - - - - - - - - - - - - - - - - - - - -
    # Living documentation

    def doc_summary(self):  # pragma: no cover
        """
        Used in living documentation.
        """
        raise NotImplementedError(self.name)

    def doc_volume_mounts(self):  # pragma: no cover
        """
        Used in living documentation.
        """
        raise NotImplementedError(self.name)

    def doc_ref(self):  # pragma: no cover
        """
        Used in living documentation.
        """
        raise NotImplementedError(self.name)

    @property
    def merkely_env_vars(self):
        """
        All the MERKELY_... env-vars for this command.
        Used in living documentation.
        """
        names = self._merkely_env_var_names
        objects = [getattr(self, name) for name in names]
        return namedtuple('MerkelyEnvVars', tuple(names))(*objects)

    @property
    def _merkely_env_var_names(self):  # pragma: no cover
        """
        The names of the MERKELY_... env-var names for
        this command, in display-order.
        Used in living documentation.
        """
        raise NotImplementedError(self.name)

    # - - - - - - - - - - - - - - - - - - - - -
    # Merkely access env-vars

    @property
    def merkelypipe(self):
        if self.name.value == "declare_pipeline":
            json = self._external.merkelypipe
        else:
            json = {}

        json["owner"] = self.owner.value
        json["name"] = self.pipeline.value
        return json

    @property
    def host(self):
        return HostEnvVar(self.env)

    @property
    def api_token(self):
        return ApiTokenEnvVar(self.env)

    @property
    def owner(self):
        return OwnerEnvVar(self.env)

    @property
    def pipeline(self):
        return PipelineEnvVar(self.env)

    # - - - - - - - - - - - - - - - - - - - - -
    # Common merkely env-vars

    @property
    def ci_build_url(self):
        return CIBuildUrlEnvVar(self.env)

    @property
    def dry_run(self):
        return DryRunEnvVar(self.env)

    @property
    def fingerprint(self):
        return FingerprintEnvVar(self._external)

    @property
    def name(self):
        return CommandNameEnvVar(self.env)

    @property
    def user_data(self):
        return UserDataEnvVar(self._external)

    @property
    def is_compliant(self):
        return IsCompliantEnvVar(self.env)

    # - - - - - - - - - - - - - - - - - - - - -
    # Subclass command implementation

    def __call__(self):  # pragma: no cover
        raise NotImplementedError(self.name)
