# freeze("$(MPY_DIR)/tools", ("upip.py", "upip_utarfile.py"))
freeze("$(MPY_DIR)/drivers/dht", "dht.py")  # noqa
freeze("$(MPY_DIR)/drivers/onewire")  # noqa

# uasyncio
include("$(MPY_DIR)/extmod/uasyncio/manifest.py")  # noqa

# drivers
freeze("$(MPY_DIR)/drivers/display", "ssd1306.py")  # noqa

# Libraries from micropython-lib, include only if the library directory exists
if os.path.isdir(convert_path("$(MPY_LIB_DIR)")):  # noqa
    # file utilities
    freeze("$(MPY_LIB_DIR)/upysh", "upysh.py")  # noqa

    # requests
    freeze("$(MPY_LIB_DIR)/urequests", "urequests.py")  # noqa
    freeze("$(MPY_LIB_DIR)/urllib.urequest", "urllib/urequest.py")  # noqa

    # umqtt
    freeze("$(MPY_LIB_DIR)/umqtt.simple", "umqtt/simple.py")  # noqa
    freeze("$(MPY_LIB_DIR)/umqtt.robust", "umqtt/robust.py")  # noqa
