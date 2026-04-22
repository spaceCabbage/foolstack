import os
import time


def generate_unique_id() -> str:
    """Generates a 26-character time-sortable ULID (Crockford's Base32)."""
    t, r = int(time.time() * 1000), int.from_bytes(os.urandom(10), "big")
    chars = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

    def b32(n, l):
        return "".join(chars[(n // (32**i)) % 32] for i in range(l - 1, -1, -1))

    return b32(t, 10) + b32(r, 16)
