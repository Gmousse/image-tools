import os
from PIL import Image, UnidentifiedImageError, ExifTags
import logging
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool
from .files import list_all_files_recursively

DEFAULT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DEFAULT_DELTA_SECONDS = 0


def init_argument_parser():
    parser = argparse.ArgumentParser(
        description="Rename images in a directory based on creation date"
    )
    parser.add_argument(
        "dir_path", type=os.path.abspath, help="The path of the directory."
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="%Y-%m-%dT%H:%M:%S",
        help="Datetime format used to rename the files.",
    )
    parser.add_argument(
        "-d",
        "--delta",
        type=int,
        default=0,
        help="An optional datetime delta in seconds to fix wrong hours or timezone.",
    )
    parser.add_argument(
        "-m",
        "--multithread",
        type=bool,
        default=True,
        help="Multithread the treatment. True by default.",
    )
    return parser


def extract_file_creation_datetime(file: "Path", delta_seconds: "int"):
    try:
        img = Image.open(str(file))
        metadata = {
            ExifTags.TAGS[k]: v
            for k, v in img.getexif().items()
            if k in ExifTags.TAGS and type(v) is not bytes
        }
        default_exif_date_fmt = "%Y:%m:%d %H:%M:%S"
        creationDate = datetime.strptime(metadata["DateTime"], default_exif_date_fmt)
    except (UnidentifiedImageError, KeyError):
        creationDate = datetime.fromtimestamp(file.stat().st_mtime)
    return creationDate + timedelta(seconds=delta_seconds)


def rename_file_by_date(
    file_path: "Path",
    datetime_format=DEFAULT_DATETIME_FORMAT,
    delta_seconds=DEFAULT_DELTA_SECONDS,
):
    creation_date = extract_file_creation_datetime(file_path, delta_seconds)
    new_file = file_path.with_name(
        creation_date.strftime(datetime_format) + file_path.suffix.lower()
    )
    logging.info("Rename {} into {}.".format(file_path.name, new_file.name))
    creation_date_str = creation_date.strftime(datetime_format)
    file_path_suffix = file_path.suffix.lower()
    increment = 0
    while new_file.exists():
        increment += 1
        new_file = file_path.with_name(
            f"{creation_date_str}_{increment}{file_path_suffix}"
        )

    file_path.rename(new_file)


def rename_files_by_date(
    dir_path: "Path",
    datetime_format=DEFAULT_DATETIME_FORMAT,
    delta_seconds=DEFAULT_DELTA_SECONDS,
    multithread=True,
):
    def _rename(file_path: "Path"):
        return rename_file_by_date(file_path, datetime_format, delta_seconds)

    files = list_all_files_recursively(dir_path)
    if multithread is True:
        pool = ThreadPool(4)
        pool.map(_rename, files)
    else:
        for file_path in files:
            _rename(file_path)


def main():
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
    args = init_argument_parser().parse_args()
    rename_files_by_date(args.path, args.format, args.delta, args.multithread)


if __name__ == "__main__":
    main()
