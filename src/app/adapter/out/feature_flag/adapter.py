from typing import Dict

from app.port.adapter.feature_flag.adapter import FeatureFlagAdapter

FLAGS: Dict[str, bool] = {}


class SimpleFeatureFlagAdapter(FeatureFlagAdapter):
    def get_flag(self, flag_name: str) -> bool:
        return FLAGS.get(flag_name, False)
