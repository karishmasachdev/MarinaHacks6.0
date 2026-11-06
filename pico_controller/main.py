from machine import Pin
import time

running_led = Pin(7, Pin.OUT)
running_led.on()

# Buttons connect GP2–GP5 to GND.
buttons = [
    Pin(2, Pin.IN, Pin.PULL_UP),
    Pin(3, Pin.IN, Pin.PULL_UP),
    Pin(4, Pin.IN, Pin.PULL_UP),
    Pin(5, Pin.IN, Pin.PULL_UP),
]

DEBOUNCE_MS = 30
raw_states = [button.value() for button in buttons]
stable_states = raw_states[:]
changed_at = [time.ticks_ms()] * len(buttons)

while True:
    now = time.ticks_ms()

    for lane, button in enumerate(buttons):
        reading = button.value()

        if reading != raw_states[lane]:
            raw_states[lane] = reading
            changed_at[lane] = now

        if (
            raw_states[lane] != stable_states[lane]
            and time.ticks_diff(now, changed_at[lane]) >= DEBOUNCE_MS
        ):
            stable_states[lane] = raw_states[lane]

            # Pull-up buttons read 0 while pressed.
            if stable_states[lane] == 0:
                print(lane)

    time.sleep_ms(5)