from __future__ import annotations
from typing import Optional

class ImageResourcesSection:
    """Represents the PSD Image Resources section as raw-preserved bytes plus unknown-only parsed summaries."""

    Empty: Optional[ImageResourcesSection] = None

    def __init__(self, raw_data, resources):
        """Initializes a new instance of the <see cref="ImageResourcesSection"/> class.

        Args:
            raw_data: The raw Image Resources payload without the section length field.
            resources: The parsed unknown resource summaries.
        """
        self.raw_data = raw_data
        self.resources = resources

    @property
    def raw_data(self):
        """Gets the raw Image Resources payload without the leading section length field."""
        return self._raw_data

    @raw_data.setter
    def raw_data(self, value):
        self._raw_data = value

    @property
    def resources(self):
        """Gets the parsed unknown-only resource blocks."""
        return self._resources

    @resources.setter
    def resources(self, value):
        self._resources = value

    @property
    def has_resources(self):
        """Gets a value indicating whether the section contains raw bytes or parsed resources."""
        return len(self.raw_data) > 0 or len(self.resources) > 0

    @classmethod
    def load(cls, reader):
        """Loads the Image Resources section from the current reader position.

        Args:
            reader: The reader positioned at the section length field.

        Returns:
            The loaded section.
        """
        resources_length = reader.ReadUInt32()
        if resources_length == 0:
            return cls.Empty

        raw_data = reader.read_bytes(resources_length, "Image Resources section")
        resources_end = len(raw_data)
        from io import BytesIO
        from aspose_psd_foss.bigendianreader import BigEndianReader
        from aspose_psd_foss.resources.unknownresource import UnknownResource
        resources_reader = BigEndianReader(BytesIO(raw_data), leave_open=True)
        resources_list = []

        while resources_reader.position < resources_end:
            resource = UnknownResource.Load(resources_reader, resources_end)
            if resource is None:
                break
            resources_list.append(resource)

        return cls(raw_data, resources_list)

    def save(self, writer):
        """Writes the Image Resources section with raw preservation when available.

        Args:
            writer: The destination writer.
        """
        if len(self.raw_data) > 0:
            writer.Write(len(self.raw_data))
            writer.Write(self.raw_data)
            return

        if len(self.resources) == 0:
            writer.Write(0)
            return

        resources_start = writer.position
        writer.Write(0)

        for resource in self.resources:
            writer.Write(0x3842494D)
            writer.Write(resource.resource_id)
            writer.WritePascalStringAlignedTo2(resource.name)
            writer.Write(len(resource.data))
            writer.Write(resource.data)

            if len(resource.data) % 2 == 1:
                writer.Write(0)

        resources_end = writer.position
        writer.seek(resources_start, 0)
        writer.Write(resources_end - resources_start - 4)
        writer.seek(resources_end, 0)


ImageResourcesSection.Empty = ImageResourcesSection([], [])
