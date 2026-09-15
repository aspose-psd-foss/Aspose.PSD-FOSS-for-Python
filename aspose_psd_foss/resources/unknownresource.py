from aspose_psd_foss.big_endian_reader import BigEndianReader
from aspose_psd_foss.psd_resource_info import PsdResourceInfo
from aspose_psd_foss.psd_resource_kind import PsdResourceKind


class UnknownResource:
    def __init__(self, resource_id: int, name: str, data: bytes):
        self.resource_id = resource_id
        self.name = name
        self.data = data

    @staticmethod
    def load(reader: BigEndianReader, section_end: int):
        start_pos = reader.position
        if start_pos + 8 > section_end:
            return None

        signature = reader.read_uint32()
        if signature != 0x3842494D:  # "8BIM"
            return None

        resource_id = reader.read_int16()
        name = reader.read_pascal_string_aligned_to_2()

        data_length = reader.read_int32()
        if data_length < 0 or reader.position + data_length > section_end:
            return None

        data = reader.read_bytes(data_length)
        if data_length % 2 == 1:
            reader.skip(1)

        return UnknownResource(resource_id, name, data)

    def to_public_info(self):
        return PsdResourceInfo(
            self.resource_id,
            self.name,
            PsdResourceKind.UNKNOWN,
            len(self.data),
            None,
            None,
        )
