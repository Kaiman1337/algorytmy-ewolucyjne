
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

from truck_route_optimizer.gui import run_gui


if __name__ == "__main__":
    run_gui()
