from __future__ import annotations

import io
from typing import List

from aspose_psd_foss.bigendianreader import BigEndianReader
from aspose_psd_foss.bigendianwriter import BigEndianWriter
from aspose_psd_foss.psdsectionreader import PsdSectionReader
from aspose_psd_foss.resources.unknownresource import UnknownResource


class ImageResourcesSection:
    """
    Represents the PSD Image Resources section as raw-preserved bytes plus unknown-only parsed summaries.
    """

    EMPTY: ImageResourcesSection = None  # will be set after class definition

    def __init__(self, raw_data: bytes, resources: List[UnknownResource]):
        self.raw_data = raw_data
        self.resources = resources

    @property
    def has_resources(self) -> bool:
        """Gets a value indicating whether the section contains raw bytes or parsed resources."""
        return len(self.raw_data) > 0 or len(self.resources) > 0

    @classmethod
    def load(cls, reader: BigEndianReader) -> ImageResourcesSection:
        """Loads the Image Resources section from the current reader position."""
        resources_length = reader.read_uint32()
        if resources_length == 0:
            return cls.EMPTY

        raw_data = PsdSectionReader.read_bytes(reader, resources_length, "Image Resources section")
        resources_end = len(raw_data)

        resources_reader = BigEndianReader(io.BytesIO(raw_data), leave_open=True)
        resources_list: List[UnknownResource] = []

        while resources_reader.position < resources_end:
            resource = UnknownResource.load(resources_reader, resources_end)
            if resource is None:
                break
            resources_list.append(resource)

        return cls(raw_data, resources_list)

    def save(self, writer: BigEndianWriter) -> None:
        """Writes the Image Resources section with raw preservation when available."""
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
        writer.seek(resources_start, 0)  # SeekOrigin.Begin == 0
        writer.write_int32(resources_end - resources_start - 4)  # sizeof(uint) == 4
        writer.seek(resources_end, 0)


# Initialize the static EMPTY instance
ImageResourcesSection.EMPTY = ImageResourcesSection(b"", [])
