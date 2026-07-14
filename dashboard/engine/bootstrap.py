from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]

APP = ROOT / "app"

#
# Make app/ importable
#
if str(APP) not in sys.path:

    sys.path.insert(

        0,

        str(APP),

    )
