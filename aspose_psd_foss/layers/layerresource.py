from abc import ABC, abstractmethod


# Represents a PSD layer resource.
class LayerResource(ABC):
    # The common layer resource signature.
    RESOURCE_SIGNATURE = 0x3842494D

    # The PSB-specific layer resource signature.
    PSB_RESOURCE_SIGNATURE = 0x38425053

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
        return self.RESOURCE_SIGNATURE

    @abstractmethod
    def save(self, stream_container, psd_version):
        """Saves the layer resource to the specified stream container.

        Args:
            stream_container: The stream container to save to.
            psd_version: The PSD version.
        """
        ...
