#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2025, 👾 17711

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import click
from pathlib import Path
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


def get_exif_datetime(image_path: Path) -> datetime | None:
    """
    Extract the creation datetime from EXIF metadata if available.

    :param image_path: Path to the image file.
    :return: Datetime object if metadata is found, otherwise None.
    """
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if not exif_data:
                return None

            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

    except Exception:
        return None

    return None


def get_file_creation_datetime(file_path: Path) -> datetime | None:
    """
    Get the file creation datetime from the file system.

    :param file_path: Path to the file.
    :return: Datetime object if available, otherwise None.
    """
    try:
        if os.name == 'nt':
            timestamp = file_path.stat().st_ctime  # Windows creation time
        else:
            timestamp = file_path.stat().st_birthtime  # macOS creation time
        return datetime.fromtimestamp(timestamp)
    except AttributeError:
        return None  # No creation time available


def generate_new_filename(file_path: Path, timestamp: datetime) -> str:
    """
    Generate a new filename based on the timestamp.

    :param file_path: Path to the original file.
    :param timestamp: Datetime object for renaming.
    :return: New filename as a string.
    """
    formatted_date = timestamp.strftime("%Y%m%d-%H%M%S")
    return f"{formatted_date}.{file_path.stem}{file_path.suffix}"


def rename_images_in_directory(directory: Path) -> None:
    """
    Rename all image files in the specified directory.

    :param directory: Path to the target directory.
    """
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            exif_datetime = get_exif_datetime(file_path)
            creation_datetime = get_file_creation_datetime(file_path)

            timestamp = exif_datetime or creation_datetime
            if not timestamp:
                click.echo(f"Skipping {file_path.name}: No date available.")
                continue

            new_filename = generate_new_filename(file_path, timestamp)
            new_path = directory / new_filename

            try:
                file_path.rename(new_path)
                click.echo(f"Renamed: {file_path.name} → {new_filename}")
            except Exception as e:
                click.echo(f"Error renaming {file_path.name}: {e}", err=True)


@click.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False, path_type=Path))
def main(directory: Path) -> None:
    """
    Rename all images in DIRECTORY based on their metadata or file creation date.
    Prioritizes EXIF metadata over system creation date.
    """
    rename_images_in_directory(directory)


if __name__ == "__main__":
    main()
