
class CiEnvVar:

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return '${' + self._name + '}'

    @property
    def string(self):
        return self._name

    def value(self, env):
        return env.get(self._name, None)
