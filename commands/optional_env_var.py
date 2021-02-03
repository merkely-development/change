
class OptionalEnvVar:
    def __init__(self, name, env):
        self._name = name
        self._env = env

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._env.get(self.name, None)

    def verify(self):
        return self
