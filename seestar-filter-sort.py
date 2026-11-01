import argparse
from pathlib import Path
import shutil
import sys

def sort_seestar_filters(target_directory: str | Path) -> None:
    ## Sort SeeStar light data into separate folders based on filters
    ## Sorting done by filename, not FITS headers in case you want to work with JPEGs

    source_dir = Path(target_directory).resolve()

    ## Handle errors
    if not source_dir.exists():
        print(f"Error: Directory '{source_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not source_dir.is_dir():
        print(f"Error: '{source_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Define target directories
    lp_dir = source_dir / "LP_Filter"
    ircut_dir = source_dir / "IRCUT_Filter"

    # Create target directories if they don't exist
    lp_dir.mkdir(exist_ok=True)
    ircut_dir.mkdir(exist_ok=True)

    ## Start counters
    lp_count = 0
    ircut_count = 0

    # Scan and move files
    for file_path in source_dir.iterdir():
        if file_path.is_file():
            filename = file_path.name

            if "_LP_" in filename:
                shutil.move(str(file_path), str(lp_dir / filename))
                lp_count += 1
            elif "_IRCUT_" in filename:
                shutil.move(str(file_path), str(ircut_dir / filename))
                ircut_count += 1

    ## Format the output summary string
    summary = (
        f"Sort complete for '{source_dir.name}':\n"
        f"  - Moved {lp_count} file(s) to {lp_dir.name}/\n"
        f"  - Moved {ircut_count} file(s) to {ircut_dir.name}/"
    )

    ## Print filter counts to console
    print(summary)

    ## Save filter counts to a text file in the working directory
    report_file = source_dir / "seestar-filter-counts.txt"
    report_file.write_text(summary + "\n", encoding="utf-8")
    print(f"\nReport written to: {report_file}")

## Main function, parse commandline/function arguments, give help description
def main():
    parser = argparse.ArgumentParser(
        description="Sort SeeStar light frames into subfolders based on filter tags (_LP_ and _IRCUT_) in the filename."
    )
    parser.add_argument(
        "-d", "--dir",
        type=str,
        required=True,
        metavar="PATH",
        help="Path to the directory containing the SeeStar light frames."
    )

    args = parser.parse_args()
    sort_seestar_filters(args.dir)


if __name__ == "__main__":
    main()