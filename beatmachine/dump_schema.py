import json

from beatmachine.effect_registry import EffectRegistry

if __name__ == "__main__":
    print(json.dumps(EffectRegistry.dump_list_schema(root=True), indent=2))
