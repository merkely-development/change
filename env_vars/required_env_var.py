from commands import CommandError
from env_vars import EnvVar


class RequiredEnvVar(EnvVar):
    """
    A required OS environment-variable.
    """
    def __init__(self, env, name, description, example=None):
        super().__init__(env, name, description, example)

    @property
    def type(self):
        return 'required'

    @property
    def value(self):
        """
        The OS env-var for name if present and non empty.
        Raises if not present or empty.
        """
        result = self.env.get(self.name, None)
        if result is None:
            raise CommandError(f"{self.name} environment-variable is not set.")
        elif result == "":
            raise CommandError(f"{self.name} environment-variable is empty string.")
        else:
            return result
