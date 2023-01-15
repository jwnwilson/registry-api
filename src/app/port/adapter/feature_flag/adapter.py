from abc import ABC


class FeatureFlagAdapter(ABC):
    def get_flag(self, flag_name: str) -> bool:
        raise NotImplementedError
