class BigEndianBitConverter:
    @staticmethod
    def to_int32(data, offset):
        return (data[offset] << 24) | (data[offset + 1] << 16) | (data[offset + 2] << 8) | data[offset + 3]
