"""APIs that offer FuriosaAI NPU devices' information and allow to control the devices"""

from furiosa_native_device import *

from furiosa.common.utils import get_sdk_version

sdk_version = get_sdk_version(__name__)


__full_version__ = "Furiosa SDK Device {} (furiosa_native_device {} {} {})".format(
    sdk_version,
    __version__,
    __git_short_hash__,
    __build_timestamp__,
)
__version__ = sdk_version


del get_sdk_version

__all__ = ["__version__", "__full_version__"]
