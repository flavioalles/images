import hashlib

from PIL import Image as PILImage


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


def resize(input_image: PILImage, width: int) -> PILImage:
    """
    Resize the input image (given an expected width) while maintaining the aspect ratio.

    Args:
        input_image (PILImage): The input image to be resized.
        width (int): The desired width of the output image.

    Returns:
        PILImage: The resized image.
    """
    height = int(float(input_image.size[1]) * (width / float(input_image.size[0])))

    return input_image.resize((width, height), PILImage.BICUBIC)
