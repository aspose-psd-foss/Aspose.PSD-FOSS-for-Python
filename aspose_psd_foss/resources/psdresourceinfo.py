from aspose_psd_foss.resources.psdresourcekind import PsdResourceKind


class PsdResourceInfo:
    """Provides a read-only summary of one parsed PSD image resource block."""

    def __init__(self, resource_id, name, kind, data_length, global_angle=None, is_icc_profile_untagged=None):
        """
        Initializes a new instance of the PsdResourceInfo class.

        :param resource_id: The PSD resource identifier.
        :param name: The decoded Pascal resource name.
        :param kind: The semantic classification exposed for the resource.
        :param data_length: The raw payload length in bytes.
        :param global_angle: The parsed global angle, when available.
        :param is_icc_profile_untagged: The parsed untagged-profile flag, when available.
        """
        self._resource_id = resource_id
        self._name = name
        self._kind = kind
        self._data_length = data_length
        self._global_angle = global_angle
        self._is_icc_profile_untagged = is_icc_profile_untagged

    @property
    def resource_id(self):
        """Gets the PSD resource identifier."""
        return self._resource_id

    @property
    def name(self):
        """Gets the decoded Pascal resource name."""
        return self._name

    @property
    def kind(self):
        """Gets the semantic classification exposed for the resource."""
        return self._kind

    @property
    def data_length(self):
        """Gets the raw payload length in bytes."""
        return self._data_length

    @property
    def global_angle(self):
        """
        Gets the parsed global angle, when this resource carries that value.
        The current unknown-only parser leaves this value unset.
        """
        return self._global_angle

    @property
    def is_icc_profile_untagged(self):
        """
        Gets the parsed untagged-profile flag, when this resource carries that value.
        The current unknown-only parser leaves this value unset.
        """
        return self._is_icc_profile_untagged
