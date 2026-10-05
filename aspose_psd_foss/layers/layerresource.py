from abc import ABC, abstractmethod
from aspose_psd_foss.streamcontainer import StreamContainer


class LayerResource(ABC):
    RESOURCE_SIGNATURE = 0x3842494D
    PSB_RESOURCE_SIGNATURE = 0x38425053

    @property
    @abstractmethod
    def key(self) -> int:
        ...

    @property
    @abstractmethod
    def length(self) -> int:
        ...

    @property
    def psd_version(self) -> int:
        return 0

    @property
    def signature(self) -> int:
        return self.RESOURCE_SIGNATURE

    @abstractmethod
    def save(self, stream_container: StreamContainer, psd_version: int) -> None:
        ...
