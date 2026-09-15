import abc
from enum import Enum, auto
from aspose_psd_foss.streamcontainer import StreamContainer


class ResourceBlock(abc.ABC):
    """
    Represents a PSD image resource block.
    """

    RESOURCE_BLOCK_SIGNATURE = 0x3842494D
    RESOURCE_BLOCK_ME_SA_SIGNATURE = 0x3842494D

    def __init__(self):
        self.id = 0
        self.name = ""

    @property
    @abc.abstractmethod
    def data_size(self) -> int:
        """
        Gets the resource data size in bytes.
        """
        ...

    @property
    @abc.abstractmethod
    def minimal_version(self) -> int:
        """
        Gets the minimal required PSD version.
        """
        ...

    @property
    def signature(self) -> int:
        """
        Gets the resource signature.
        """
        return self.RESOURCE_BLOCK_SIGNATURE

    @property
    def size(self) -> int:
        """
        Gets the resource block size in bytes including its data.
        """
        return self.data_size

    @abc.abstractmethod
    def save(self, stream: StreamContainer):
        """
        Saves the resource block to the specified stream container.

        :param stream: The stream container to save to.
        """
        ...

    def validate_values(self):
        """
        Validates the resource values.
        """
        pass


class ResourceBlockState(Enum):
    """
    Represents resource block state.
    """

    READY = auto()
    DISPOSED = auto()

