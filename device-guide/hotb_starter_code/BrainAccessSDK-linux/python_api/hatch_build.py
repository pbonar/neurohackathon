import platform
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

def get_platform_tag():
    system = platform.system()
    if system == "Linux":
        return "linux_x86_64"
    elif system == "Darwin":
        return "macosx_10_9_x86_64"
    elif system == "Windows":
        return "win_amd64"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        build_data['tag'] = f'py3-none-{get_platform_tag()}'
