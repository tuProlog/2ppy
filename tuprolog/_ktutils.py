import logging
from jpype import JImplementationFor

from collections.abc import Iterable

@JImplementationFor("kotlin.sequences.Sequence")
class _KtSequence:
    def __jclass_init__(self):
       Iterable.register(self)

    def __iter__(self):
       return self.iterator()

logging.debug("Configure Kt-specific extensions")
