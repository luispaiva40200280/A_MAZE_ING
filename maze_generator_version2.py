import random
import os
import sys
import termios

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
print(old_settings)

print(os.get_terminal_size().__doc__)
value = 15
value &= ~4
print(bin(value))
print(value)

seed = 42
rng = random.Random(seed)
print(rng.randint(10, 100))
print(rng.randint(10, 100))
print(rng.randint(10, 100))
print(rng.randint(10, 100))
