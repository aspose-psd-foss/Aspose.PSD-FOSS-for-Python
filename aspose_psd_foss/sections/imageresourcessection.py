from typing import Optional

# Represents the PSD Image Resources section as raw-preserved bytes plus unknown-only parsed summaries.
class ImageResourcesSection:
    """
    Represents the PSD Image Resources section as raw-preserved bytes plus unknown-only parsed summaries.
    """

    # Gets an empty Image Resources section.
    EMPTY: Optional["ImageResourcesSection"] = None

    def __init__(self, raw_data: bytes, resources):
        """
        Initializes a new instance of the ImageResourcesSection class.

        :param raw_data: The raw Image Resources payload without the section length field.
        :param resources: The parsed unknown resource summaries.
        """
        self.raw_data = raw_data
        self.resources = resources

    # Gets the raw Image Resources payload without the leading section length field.
    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self, value):
        self._raw_data = value

    # Gets the parsed unknown-only resource blocks.
    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, value):
        self._resources = value

    # Gets a value indicating whether the section contains raw bytes or parsed resources.
    @property
    def has_resources(self):
        return len(self.raw_data) > 0 or len(self.resources) > 0

    # Loads the Image Resources section from the current reader position.
    @staticmethod
    def load(reader):
        """
        Loads the Image Resources section from the current reader position.

        :param reader: The reader positioned at the section length field.
        :return: The loaded section.
        """
        from aspose_psd_foss.bigendianreader import BigEndianReader
        from aspose_psd_foss.psdsectionreader import PsdSectionReader
        from aspose_psd_foss.resources.unknownresource import UnknownResource

        resources_length = reader.read_uint32()
        if resources_length == 0:
            return ImageResourcesSection.EMPTY

        raw_data = PsdSectionReader.read_bytes(
            reader, resources_length, "Image Resources section"
        )
        resources_end = len(raw_data)
        resources_reader = BigEndianReader(
            memoryview(raw_data), leave_open=True
        )
        resources_list = []

        while resources_reader.position < resources_end:
            resource = UnknownResource.load(resources_reader, resources_end)
            if resource is None:
                break
            resources_list.append(resource)

        return ImageResourcesSection(raw_data, resources_list)

    # Writes the Image Resources section with raw preservation when available.
    def save(self, writer):
        """
        Writes the Image Resources section with raw preservation when available.

        :param writer: The destination writer.
        """
        from aspose_psd_foss.bigendianwriter import BigEndianWriter

        if len(self.raw_data) > 0:
            writer.write_uint32(len(self.raw_data))
            writer.write(self.raw_data)
            return

        if len(self.resources) == 0:
            writer.write_uint32(0)
            return

        resources_start = writer.position
        writer.write_uint32(0)

        for resource in self.resources:
            writer.write_uint32(0x3842494D)
            writer.write_int16(resource.resource_id)
            writer.write_pascal_string_aligned_to_2(resource.name)
            writer.write_int32(len(resource.data))
            writer.write(resource.data)

            if len(resource.data) % 2 == 1:
                writer.write_uint8(0)

        resources_end = writer.position
        writer.seek(resources_start, 0)  # SeekOrigin.Begin = 0
        writer.write_uint32(resources_end - resources_start - 4)
        writer.seek(resources_end, 0)


# Initialize the EMPTY static instance
ImageResourcesSection.EMPTY = ImageResourcesSection(b"", [])
