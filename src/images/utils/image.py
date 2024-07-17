import hashlib


def sha256_checksum(path: str) -> str:
    """
    Calculate the SHA256 checksum of a file.

    Args:
        path (str): The path to the file.

    Returns:
        str: The SHA256 checksum of the file.
    """
    sha256 = hashlib.sha256()

    with open(path, "rb") as image:
        for block in iter(lambda: image.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()
