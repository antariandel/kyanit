freeze("$(PORT_DIR)/boards/KYANIT/modules")  # noqa

# drivers
freeze("$(MPY_DIR)/drivers/display", "ssd1306.py")  # noqa
freeze("$(MPY_DIR)/drivers/dht", "dht.py")  # noqa
freeze("$(MPY_DIR)/drivers/onewire")  # noqa

# file utilities
freeze("$(MPY_LIB_DIR)/upysh", "upysh.py")  # noqa

# uasyncio
include("$(MPY_DIR)/extmod/uasyncio/manifest.py")  # noqa

# requests
freeze("$(MPY_LIB_DIR)/urequests", "urequests.py")  # noqa
freeze("$(MPY_LIB_DIR)/urllib.urequest", "urllib/urequest.py")  # noqa

# umqtt
freeze("$(MPY_LIB_DIR)/umqtt.simple", "umqtt/simple.py")  # noqa
freeze("$(MPY_LIB_DIR)/umqtt.robust", "umqtt/robust.py")  # noqa
