import pygame
import serial


LANE_KEYS = {
    pygame.K_d: 0,
    pygame.K_f: 1,
    pygame.K_j: 2,
    pygame.K_k: 3,
}

HARDWARE_LANE_EVENT = pygame.USEREVENT + 1

_serial_connection = None
_serial_buffer = b""


def init_hardware(port):
    """Open the Pico's USB serial connection."""
    global _serial_connection

    _serial_connection = serial.Serial(
        port=port,
        baudrate=115200,
        timeout=0,
    )


def poll_hardware_input():
    """Read lane numbers from the Pico and add them to Pygame's event queue."""
    global _serial_buffer

    if _serial_connection is None:
        return

    waiting = _serial_connection.in_waiting
    if waiting == 0:
        return

    _serial_buffer += _serial_connection.read(waiting)
    lines = _serial_buffer.split(b"\n")
    _serial_buffer = lines.pop()

    for line in lines:
        try:
            lane = int(line.strip())
        except ValueError:
            continue

        if 0 <= lane <= 3:
            print(f"Received Pico lane: {lane}")
            pygame.event.post(
                pygame.event.Event(HARDWARE_LANE_EVENT, lane=lane)
            )


def get_lane_from_event(event):
    """Return a lane for a keyboard or Pico button press, otherwise None."""
    if event.type == HARDWARE_LANE_EVENT:
        return event.lane

    if event.type == pygame.KEYDOWN:
        return LANE_KEYS.get(event.key)

    return None


def close_hardware():
    """Close the Pico connection when the game exits."""
    if _serial_connection is not None:
        _serial_connection.close()