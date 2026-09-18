import abc
from enum import Enum
from aspose_psd_foss.streamcontainer import StreamContainer


class ResourceBlock(abc.ABC):
    """Represents a PSD image resource block."""

    RESOURCE_BLOCK_SIGNATURE = 0x3842494D
    RESOURCE_BLOCK_ME_SA_SIGNATURE = 0x3842494D

    def __init__(self):
        self._id: int = 0
        self._name: str = ""

    @property
    def id(self) -> int:
        """Gets or sets the unique identifier for the resource."""
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def name(self) -> str:
        """Gets or sets the resource name."""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def signature(self) -> int:
        """Gets the resource signature."""
        return self.RESOURCE_BLOCK_SIGNATURE

    @property
    @abc.abstractmethod
    def data_size(self) -> int:
        """Gets the resource data size in bytes."""
        ...

    @property
    @abc.abstractmethod
    def minimal_version(self) -> int:
        """Gets the minimal required PSD version."""
        ...

    @property
    def size(self) -> int:
        """Gets the resource block size in bytes including its data."""
        return self.data_size

    @abc.abstractmethod
    def save(self, stream: StreamContainer):
        """Saves the resource block to the specified stream container."""
        ...

    def validate_values(self):
        """Validates the resource values."""
        pass

    class ResourceBlockState(Enum):
        """Represents resource block state."""
        READY = 0
        DISPOSED = 1
