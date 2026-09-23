from abc import ABC, abstractmethod
from aspose_psd_foss.streamcontainer import StreamContainer


class ResourceBlock(ABC):
    """
    Represents a PSD image resource block.
    """

    #: The regular Photoshop resource signature.
    RESOURCE_BLOCK_SIGNATURE = 0x3842494D

    #: The ImageReady resource signature.
    RESOURCE_BLOCK_ME_SA_SIGNATURE = 0x3842494D

    def __init__(self):
        self._id = 0
        self._name = ""

    @property
    @abstractmethod
    def data_size(self):
        """
        Gets the resource data size in bytes.
        """
        pass

    @property
    def id(self):
        """
        Gets or sets the unique identifier for the resource.
        """
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    @abstractmethod
    def minimal_version(self):
        """
        Gets the minimal required PSD version.
        """
        pass

    @property
    def name(self):
        """
        Gets or sets the resource name.
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def signature(self):
        """
        Gets the resource signature.
        """
        return self.RESOURCE_BLOCK_SIGNATURE

    @property
    def size(self):
        """
        Gets the resource block size in bytes including its data.
        """
        return self.data_size

    @abstractmethod
    def save(self, stream):
        """
        Saves the resource block to the specified stream container.
        
        :param stream: The stream container to save to.
        """
        pass

    def validate_values(self):
        """
        Validates the resource values.
        """
        pass

    class ResourceBlockState:
        """
        Represents resource block state.
        """

        #: The resource block is ready.
        READY = 0

        #: The resource block is disposed.
        DISPOSED = 1
