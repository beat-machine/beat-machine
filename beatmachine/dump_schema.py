import json
import sys
from beatmachine.effects.base import EffectRegistry

if __name__ == "__main__":
    print(json.dumps(EffectRegistry.dump_list_schema(root=True), indent=2))
    sys.exit(0)
