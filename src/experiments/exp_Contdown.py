'''
A little countdown app
'''
from rich import print as rprint
from rich import inspect
from datetime import datetime as dt
import argparse
import winsound
import time


def main(sec: int) -> None:
    '''Main entry point of the script'''
    start = dt.now()
    while True: 
        time.sleep(1)
        
        difference = dt.now() - start
        #inspect(difference)
        print(f"Time elapsed: {difference} secs.")
        if difference.total_seconds() > sec:
            start = dt.now()
            winsound.Beep(1000, 3000)  # Frequency: 1000Hz, Duration: 1000ms

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Countdown App")
    parser.add_argument(
        "--minutes", "-m",
        type=int,
        default=10,
        help="Time to countdown in seconds (default: 10)",
    )
    parser.add_argument(
        "--seconds", "-s",
        type=int,
        default=30,
        help="Time to countdown in seconds (default: 30)",
    )
    args = parser.parse_args()
    sec = args.minutes * 60 + args.seconds
    main(sec)
