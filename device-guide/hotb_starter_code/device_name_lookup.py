from brainaccess import core

def name_lookup() -> None:
    core.init()

    devices = core.scan()

    if devices:
        print(f"Available devices: {[device.name for device in devices]}")
    else:
        print("No devices were found!")

    core.close()

if __name__ == "__main__":
    name_lookup()
