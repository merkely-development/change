from abc import ABC, abstractmethod


class Fingerprinter(ABC):

    @abstractmethod
    def handles_protocol(self, string):
        """
        Returns True iff string starts with the class's protocol.
        """
        pass

    @abstractmethod
    def artifact_name(self, string):
        """
        Returns the artifact_name from after the protocol string.
        Raises if handles_protocol(string) is False.
        """
        pass

    @abstractmethod
    def artifact_basename(self, string):
        """
        Returns the artifact_basename from after the protocol string.
        Raises if handles_protocol(string) is False.
        """
        pass

    @abstractmethod
    def sha(self, protocol, artifact_name):
        """
        Returns the sha for the artifact_name.
        Raises if handles_protocol(string) is False.
        """
        pass
