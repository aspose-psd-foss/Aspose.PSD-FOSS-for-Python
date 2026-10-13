# aspose_psd_foss/layers/layermaskinfo.py
class LayerMaskInfo:
    def __init__(self, is_present, raw_data_length):
        self._is_present = is_present
        self._raw_data_length = raw_data_length

    @property
    def is_present(self):
        return self._is_present

    @property
    def raw_data_length(self):
        return self._raw_data_length
