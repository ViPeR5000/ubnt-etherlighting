from random import randint
from etherlight import Etherlight

etherlight = Etherlight("10.0.10.6")

# for i in range(48):
#     etherlight.set_led_color(i + 1, (0, 10, 0))
#     # time.sleep(0.1)
# etherlight.flush()

# time.sleep(5)
# for _i in range(15):
#     for c in [(10, 0, 0), (0, 10, 0), (0, 0, 10)]:
#         for i in range(48):
#             etherlight.cache_led_color(i + 1, c)
#         etherlight.flush_led_cache()
while True:
    led_colors = [(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(52)]
    etherlight.set_led_colors(led_colors)  # Set all colors in a single call
    etherlight.flush()

