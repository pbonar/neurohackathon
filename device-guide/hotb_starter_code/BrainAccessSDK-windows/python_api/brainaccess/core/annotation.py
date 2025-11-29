import ctypes


class Annotation(ctypes.Structure):
    """Represents a single annotation with a timestamp and text.

    This class is used to mark specific points in time with a descriptive
    label, which is useful for synchronizing EEG data with external events.

    Attributes
    ----------
    timestamp : int
        The sample number corresponding to the time the annotation was recorded.
        This allows for precise alignment with the EEG data stream.
    annotation : str
        The text of the annotation, decoded from ASCII. This provides a human-readable
        description of the event that occurred at the given timestamp.
    """
    _fields_ = [
        ("timestamp", ctypes.c_size_t),
        ("_annotation", ctypes.c_char_p),
    ]

    @property
    def annotation(self):
        """The annotation text, decoded from ASCII."""
        return self._annotation.decode('ascii')
