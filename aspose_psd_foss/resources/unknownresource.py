# Represents a parsed PSD image resource block without any ID‑specific semantics.
class UnknownResource:
    """Initializes a new instance of the UnknownResource class.

    Args:
        resource_id: The PSD resource identifier.
        name: The decoded Pascal resource name.
        data: The raw resource payload.
    """
    def __init__(self, resource_id, name, data):
        self._resource_id = resource_id
        self._name = name
        self._data = data

    @property
    def resource_id(self):
        """Gets the PSD resource identifier."""
        return self._resource_id

    @property
    def name(self):
        """Gets the decoded Pascal resource name."""
        return self._name

    @property
    def data(self):
        """Gets the raw resource payload bytes."""
        return self._data

    @property
    def ResourceId(self):
        return self._resource_id

    @property
    def Name(self):
        return self._name

    @property
    def Data(self):
        return self._data

    @classmethod
    def load(cls, reader, section_end):
        """Attempts to load one resource block from the reader.

        Args:
            reader: The reader positioned at the start of a resource block.
            section_end: The byte position of the end of the resources section.

        Returns:
            An UnknownResource instance or None if parsing cannot continue safely.
        """
        start_pos = reader.Position
        if start_pos + 8 > section_end:
            return None

        signature = reader.ReadUInt32()
        if signature != 0x3842494D:  # "8BIM"
            return None

        resource_id = reader.ReadInt16()
        name = reader.ReadPascalStringAlignedTo2()

        data_length = reader.ReadInt32()
        if data_length < 0 or reader.Position + data_length > section_end:
            return None

        data = reader.ReadBytes(data_length)
        if data_length % 2 == 1:
            reader.Skip(1)

        return cls(resource_id, name, data)

    @classmethod
    def Load(cls, reader, section_end):
        return cls.load(reader, section_end)

    def to_public_info(self):
        """Creates a public read‑only summary for this resource block.

        Returns:
            The public PsdResourceInfo summary with PsdResourceKind.Unknown.
        """
        from aspose_psd_foss.resources.psdresourceinfo import PsdResourceInfo
        from aspose_psd_foss.resources.psdresourcekind import PsdResourceKind
        return PsdResourceInfo(
            self.resource_id,
            self.name,
            PsdResourceKind.Unknown,
            len(self.data),
            None,
            None,
        )
