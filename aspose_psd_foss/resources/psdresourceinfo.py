class PsdResourceInfo:
    def __init__(self, resource_id, name, kind, data_length, global_angle=None, is_icc_profile_untagged=None):
        self.resource_id = resource_id
        self.name = name
        self.kind = kind
        self.data_length = data_length
        self.global_angle = global_angle
        self.is_icc_profile_untagged = is_icc_profile_untagged

    @property
    def resource_id(self):
        return self._resource_id

    @resource_id.setter
    def resource_id(self, value):
        self._resource_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        self._kind = value

    @property
    def data_length(self):
        return self._data_length

    @data_length.setter
    def data_length(self, value):
        self._data_length = value

    @property
    def global_angle(self):
        return self._global_angle

    @global_angle.setter
    def global_angle(self, value):
        self._global_angle = value

    @property
    def is_icc_profile_untagged(self):
        return self._is_icc_profile_untagged

    @is_icc_profile_untagged.setter
    def is_icc_profile_untagged(self, value):
        self._is_icc_profile_untagged = value
