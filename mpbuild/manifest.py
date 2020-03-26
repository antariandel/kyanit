freeze("$(PORT_DIR)/boards/KYANIT/modules")
freeze("$(MPY_DIR)/drivers/dht", "dht.py")
freeze("$(MPY_DIR)/drivers/onewire")

# drivers
freeze("$(MPY_DIR)/drivers/display", "ssd1306.py")

# file utilities
freeze("$(MPY_LIB_DIR)/upysh", "upysh.py")

# uasyncio
include("$(MPY_DIR)/extmod/uasyncio/manifest.py")
freeze("$(MPY_LIB_DIR)/uasyncio", "uasyncio/__init__.py")
freeze("$(MPY_LIB_DIR)/uasyncio.core", "uasyncio/core.py")

# requests
freeze("$(MPY_LIB_DIR)/urequests", "urequests.py")
freeze("$(MPY_LIB_DIR)/urllib.urequest", "urllib/urequest.py")

# umqtt
freeze("$(MPY_LIB_DIR)/umqtt.simple", "umqtt/simple.py")
freeze("$(MPY_LIB_DIR)/umqtt.robust", "umqtt/robust.py")
