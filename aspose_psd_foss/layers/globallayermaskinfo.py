# Represents global layer mask information.
class GlobalLayerMaskInfo:
    Empty: GlobalLayerMaskInfo = GlobalLayerMaskInfo()

    @classmethod
    def empty(cls):
        return cls()

