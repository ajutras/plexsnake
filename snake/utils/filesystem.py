import os
from typing import List


def list_folder_content(path: str) -> List[str]:
    return sorted([filename for filename in os.listdir(path)])
