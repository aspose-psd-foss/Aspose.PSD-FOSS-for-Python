# aspose_psd_foss/src/resources/preserved_resource_block.py

from aspose_psd_foss.resource_block import ResourceBlock
from aspose_psd_foss.resources.unknown_resource import UnknownResource
from aspose_psd_foss.psd_version import PsdVersion
from aspose_psd_foss.stream_container import StreamContainer


class PreservedResourceBlock(ResourceBlock):
    """
    Adapts a raw-preserved image resource to the official ResourceBlock surface.
    """

    # Stores the preserved resource payload.
    def __init__(self, resource: UnknownResource):
        """
        Initializes a new instance of the PreservedResourceBlock class.

        :param resource: The parsed raw resource block.
        """
        self.id = resource.resource_id
        self.name = resource.name
        self._data = resource.data

    @property
    def data_size(self) -> int:
        """Gets the resource data size in bytes."""
        return len(self._data)

    @property
    def minimal_version(self) -> int:
        """Gets the minimal required PSD version."""
        return int(PsdVersion.PSD)

    def save(self, stream: StreamContainer):
        """
        Saves the resource block to the specified stream container.

        :param stream: The stream container to save to.
        """
        raise NotImplementedError(
            "Saving individual image resource blocks is not supported by this FOSS build."
        )
