import argparse
from pathlib import Path
from astropy.io import fits

def calculate_total_exposure(folder_path):
    total_seconds = 0.0
    file_count = 0
    path = Path(folder_path)
    
    # We use rglob here just in case you have subfolders (e.g., lights/night1, lights/night2)
    for fits_file in path.rglob('*.fit*'):
        try:
            with fits.open(fits_file) as hdul:
                header = hdul[0].header
                exposure = header.get('EXPTIME') or header.get('EXPOSURE')
                
                if exposure is not None:
                    total_seconds += float(exposure)
                    file_count += 1
                else:
                    print(f"Warning: No exposure keyword found in {fits_file.name}")
        except Exception as e:
            print(f"Error processing {fits_file.name}: {e}")

    return total_seconds, file_count

def main():
    # Set up the command line arguments
    parser = argparse.ArgumentParser(description="Calculate total exposure time for FITS files.")
    parser.add_argument("-d", "--directory", type=str, required=True,
                        help="The working directory (e.g., /Users/name/Pictures/Target)")
    
    args = parser.parse_args()

    # Setup paths based on the user input
    working_directory = Path(args.directory)
    lights_folder = working_directory / "lights"
    output_file = working_directory / "exposure_total.txt"

    # Validation: Make sure the 'lights' folder actually exists
    if not lights_folder.exists():
        print(f"Error: Could not find a 'lights' folder inside {working_directory}")
        return

    # Run the calculation
    total_s, count = calculate_total_exposure(lights_folder)

    # Prepare the report string
    report = (
        f"--- Summary ---\n"
        f"Folder processed: {lights_folder}\n"
        f"Files processed: {count}\n"
        f"Total Exposure:  {total_s:.2f} seconds\n"
        f"Total Exposure:  {total_s / 3600:.2f} hours\n"
    )

    # Print to console
    print(report)

    # Save to the text file
    with open(output_file, "w") as f:
        f.write(report)

    print(f"Textfile saved to {output_file}")

if __name__ == "__main__":
    main()