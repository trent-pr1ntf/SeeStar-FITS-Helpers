import argparse
from astropy.io import fits
from pathlib import Path

def get_seestar_info(file_path):
    path = Path(file_path)
    
    if not path.is_file():
        print(f"Error: File {file_path} not found.")
        return

    try:
        with fits.open(path) as hdul:
            header = hdul[0].header
            
            stack_count = header.get('STACKCNT', 'Not Found')
            live_time = header.get('LIVETIME', 0)
            
            print(f"\n--- SeeStar File Info: {path.name} ---")
            print(f"Stack Count:  {stack_count}")
            
            if live_time > 0:
                # Calculations
                minutes = live_time / 60
                hours_raw = live_time / 3600
                hours_rounded = round(hours_raw)
                
                print(f"Seconds:      {live_time}s")
                print(f"Minutes:      {minutes:.2f}m")
                print(f"Exact Hours:  {hours_raw:.2f}h")
                print(f"Rounded:      ~{hours_rounded} hour(s)")
            else:
                print("Live Time:    Keyword 'LIVETIME' not found or is zero.")

    except Exception as e:
        print(f"Error reading SeeStar FITS: {e}")

def main():
    parser = argparse.ArgumentParser(description="Read SeeStar STACKCNT and LIVETIME.")
    parser.add_argument("-i", "--input", type=str, required=True, 
                        help="Path to the SeeStar FITS file")
    
    args = parser.parse_args()
    get_seestar_info(args.input)

if __name__ == "__main__":
    main()