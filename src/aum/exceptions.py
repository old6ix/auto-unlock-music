from typing import Optional


class PatchSizeError(ValueError):
    def __init__(self, patch_size: int, message: Optional[str] = None):
        if message is None:
            super().__init__(f'Patch size must be non-negative (value: {patch_size}).')
        else:
            super().__init__(message)
