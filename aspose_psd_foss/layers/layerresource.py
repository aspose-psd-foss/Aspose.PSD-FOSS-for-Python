from abc import ABC, abstractmethod
from aspose_psd_foss.streamcontainer import StreamContainer


class LayerResource(ABC):
    """Represents a PSD layer resource."""

    ResourceSignature = 0x3842494D
    PsbResourceSignature = 0x38425053

    @property
    @abstractmethod
    def key(self):
        """Gets the layer resource key."""
        ...

    @property
    @abstractmethod
    def length(self):
        """Gets the layer resource length in bytes."""
        ...

    @property
    def psd_version(self):
        """Gets the minimal PSD version required for the layer resource."""
        return 0

    @property
    def signature(self):
        """Gets the layer resource signature."""
        return self.ResourceSignature

    @abstractmethod
    def save(self, stream_container: StreamContainer, psd_version: int):
        """Saves the layer resource to the specified stream container."""
        ...
