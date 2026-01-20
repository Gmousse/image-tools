import os
import argparse
from pathlib import Path
from PIL import Image
import pyheif
import logging
from multiprocessing.pool import ThreadPool
from .files import list_all_files_recursively

QUALITY = 100


def init_argument_parser():
    parser = argparse.ArgumentParser(
        description="Convert HEIC files to JPG in a directory"
    )
    parser.add_argument(
        "dir_path", type=os.path.abspath, help="The path of the directory."
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=QUALITY,
        help="Quality of the output JPG (1-100). Default is 100.",
    )
    parser.add_argument(
        "-m",
        "--multithread",
        type=bool,
        default=True,
        help="Multithread the treatment. True by default.",
    )
    return parser


def convert_heic_image_to_jpg(file_path: "Path", quality=QUALITY):
    try:
        heifFile = pyheif.read(file_path)
        image = Image.frombytes(
            heifFile.mode,
            heifFile.size,
            heifFile.data,
            "raw",
            heifFile.mode,
            heifFile.stride,
        )
        jpgFile = file_path.with_suffix(".jpg")
        image.save(jpgFile, "JPEG", quality=quality)
        logging.info(f"Converted {file_path.name} to {jpgFile.name}")
    except Exception as e:
        logging.error(f"Failed to convert {file_path.name}: {e}")


def is_heic_file(file_path: "Path"):
    return file_path.suffix.lower() == ".heic"


def convert_heic_images_to_jpg(dir_path: "Path", quality=QUALITY, multithread=True):
    def _convert(file_path: "Path"):
        if is_heic_file(file_path):
            return convert_heic_image_to_jpg(file_path, quality)

    files = list_all_files_recursively(dir_path)
    if multithread:
        pool = ThreadPool(4)
        pool.map(_convert, files)
    else:
        for file_path in files:
            _convert(file_path)


def main():
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
    args = init_argument_parser().parse_args()
    convert_heic_images_to_jpg(args.dir_path, args.quality, args.multithread)


if __name__ == "__main__":
    main()
