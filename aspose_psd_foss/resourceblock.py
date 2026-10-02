from __future__ import annotations

import abc
from abc import ABC, abstractmethod
from enum import Enum, auto


class ResourceBlock(ABC):
    """
    Represents a PSD image resource block.
    """
    # The regular Photoshop resource signature.
    RESOURCE_BLOCK_SIGNATURE = 0x3842494D
    # The ImageReady resource signature.
    RESOURCE_BLOCK_MESA_SIGNATURE = 0x3842494D

    def __init__(self):
        # Gets or sets the unique identifier for the resource.
        self.id: int = 0
        # Gets or sets the resource name.
        self.name: str = ""

    @property
    @abstractmethod
    def data_size(self) -> int:
        """
        Gets the resource data size in bytes.
        """
        ...

    @property
    @abstractmethod
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

    @abstractmethod
    def save(self, stream) -> None:
        """
        Saves the resource block to the specified stream container.

        :param stream: The stream container to save to.
        """
        # Local import to avoid circular dependencies
        from aspose_psd_foss.streamcontainer import StreamContainer
        ...

    def validate_values(self) -> None:
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

