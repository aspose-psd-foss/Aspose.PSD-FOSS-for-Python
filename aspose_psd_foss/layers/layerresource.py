class LayerResource:
    """Represents a PSD layer resource."""

    RESOURCE_SIGNATURE = 0x3842494D
    """The common layer resource signature."""

    PSB_RESOURCE_SIGNATURE = 0x38425053
    """The PSB-specific layer resource signature."""

    @property
    def key(self):
        """Gets the layer resource key."""
        raise NotImplementedError()

    @property
    def length(self):
        """Gets the layer resource length in bytes."""
        raise NotImplementedError()

    @property
    def psd_version(self):
        """Gets the minimal PSD version required for the layer resource."""
        return 0

    @property
    def signature(self):
        """Gets the layer resource signature."""
        return LayerResource.RESOURCE_SIGNATURE

    def save(self, stream_container, psd_version):
        """Saves the layer resource to the specified stream container.

        :param stream_container: The stream container to save to.
        :param psd_version: The PSD version.
        """
        raise NotImplementedError()
