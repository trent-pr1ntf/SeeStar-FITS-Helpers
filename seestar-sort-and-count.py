### SeeStar Sort and Count
## Sort raw light data by filters, and total the integration time

## Import stuff
import argparse
from pathlib import Path
import shutil
import sys

# Standard astropy import for reading FITS header metadata
try:
    from astropy.io import fits
except ImportError:
    print("Error: 'astropy' is required to read FITS headers. Install it via 'pip install astropy'.", file=sys.stderr)
    sys.exit(1)

## FITS handling function
def get_fits_exposure(file_path: Path) -> float:
    ## Reads the exposure time directly from the FITS primary header.
    ## Looks for standard keywords 'EXPOSURE' or 'EXPTIME'. Returns 0.0 if not found.
    
    try:
        with fits.open(file_path, mode="readonly") as hdul:
            header = hdul[0].header
            # Return EXPOSURE or EXPTIME key if present
            if "EXPOSURE" in header:
                return float(header["EXPOSURE"])
            elif "EXPTIME" in header:
                return float(header["EXPTIME"])
    except Exception:
        # Handles corrupt files or non-FITS formats safely
        pass
    return 0.0

## Directory integration totaling function
def calculate_folder_metrics(folder_path: Path) -> tuple[int, float]:
    ## Scans a folder and returns total file count and accumulated exposure seconds
    count = 0
    total_seconds = 0.0

    if folder_path.exists() and folder_path.is_dir():
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                count += 1
                total_seconds += get_fits_exposure(file_path)

    return count, total_seconds

## Sorting and counting function
def sort_seestar_filters(target_directory: str | Path) -> None:
    ## Sort SeeStar light data into separate folders based on filters
    ## Calculates exposure metrics directly from FITS headers

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

    ## Track files moved during this run
    lp_moved = 0
    ircut_moved = 0

    # Scan root directory and move files into filter subfolders
    for file_path in list(source_dir.iterdir()):
        if file_path.is_file():
            filename = file_path.name

            if "_LP_" in filename:
                shutil.move(str(file_path), str(lp_dir / filename))
                lp_moved += 1
            elif "_IRCUT_" in filename:
                shutil.move(str(file_path), str(ircut_dir / filename))
                ircut_moved += 1

    ## Calculate totals directly from the target folders POST-move
    lp_count, total_lp_seconds = calculate_folder_metrics(lp_dir)
    ircut_count, total_ircut_seconds = calculate_folder_metrics(ircut_dir)

    # Rounded hour calculations for each filter and total
    lp_hours_rounded = round(total_lp_seconds / 3600.0)
    ircut_hours_rounded = round(total_ircut_seconds / 3600.0)

    # Totals across all light frames in subfolders
    total_files = lp_count + ircut_count
    total_seconds = total_lp_seconds + total_ircut_seconds
    total_hours_rounded = round(total_seconds / 3600.0)

    ## Format the output summary string
    summary = (
        f"  SeeStar Filter & Integration Summary: {source_dir.name}\n"
        f"  - Newly Moved Frames       : {lp_moved} LP | {ircut_moved} IRCUT\n"
        f"  - LP Filter Total Files    : {lp_count} ({total_lp_seconds:.1f}s | ~{lp_hours_rounded} hrs)\n"
        f"  - IRCUT Filter Total Files : {ircut_count} ({total_ircut_seconds:.1f}s | ~{ircut_hours_rounded} hrs)\n"
        f"  - Total Light Frames       : {total_files}\n"
        f"  - Total Integration Time   : {total_seconds:.1f} seconds\n"
        f"  - Total Integration (Hours): {total_hours_rounded} hour(s) (rounded)\n"
    )

    ## Print filter counts and integration metrics to console
    print(summary)

    ## Save report to a text file in the working directory
    report_file = source_dir / "seestar-integration-and-counts.txt"
    report_file.write_text(summary + "\n", encoding="utf-8")
    print(f"\nReport written to: {report_file}")


## Main function, parse commandline/function arguments, give help description
def main():
    parser = argparse.ArgumentParser(
        description="Sort SeeStar light frames into filter folders and compute integration time directly from FITS headers."
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
