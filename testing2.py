import logging
import argparse

p = argparse.ArgumentParser()

logging_level = 0

print(f"level: {logging_level}")

logging.basicConfig(
    format="%(levelname)s - %(message)s", level=logging.getLevelName(logging_level),
)

logging.debug("test")
logging.debug("\ntest2")
