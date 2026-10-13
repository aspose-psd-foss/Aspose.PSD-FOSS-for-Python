from aspose_psd_foss.resourceblock import ResourceBlock
from aspose_psd_foss.streamcontainer import StreamContainer
from aspose_psd_foss.psdversion import PsdVersion
from aspose_psd_foss.resources.unknownresource import UnknownResource


class PreservedResourceBlock(ResourceBlock):
    """Adapts a raw‑preserved image resource to the official ResourceBlock surface."""

    def __init__(self, resource: UnknownResource):
        self.id = resource.resource_id
        self.name = resource.name
        self._data = resource.data

    @property
    def data_size(self) -> int:
        return len(self._data)

    @property
    def minimal_version(self) -> int:
        return int(PsdVersion.Psd)

    def save(self, stream: StreamContainer) -> None:
        raise NotImplementedError(
            "Saving individual image resource blocks is not supported by this FOSS build."
        )
