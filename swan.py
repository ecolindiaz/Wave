import os
import subprocess

def create_swan_input_file(wind_file, bathymetry_file, swan_input_filename="swan_input.swn"):
    with open(swan_input_filename, "w") as f:
        f.write("Project 'DeliWaves' 'SWAN model'\n")
        f.write("SET LEVEL 1\n")
        f.write("MODE NONSTATIONARY\n")

        # Time settings
        f.write("CGRID REG 0.0 0.01 50 0.0 0.01 50 0.0 360.0 36\n")

        # Bathymetry
        f.write(f"READ BATHYMETRY 1 '{bathymetry_file}' 1 0\n")

        # Wind
        f.write(f"READ WIND 1 '{wind_file}' 1 0\n")

        # Boundary conditions (you can adjust as needed)
        f.write("BOUND SHAPE JONSWAP PEAK 3.3\n")
        f.write("GEN3\n")
        f.write("BREAKING 0.73\n")

        # Output
        f.write("TABLE OUT 'output_table.txt'\n")
        f.write("COMPUTE 1 HR 1\n")
        f.write("STOP\n")

    print(f"[✓] SWAN input file created: {swan_input_filename}")
    return swan_input_filename

def run_swan(swan_input_filename):
    print(f"[▶] Running SWAN with {swan_input_filename}")
    result = subprocess.run(["swanrun", swan_input_filename], capture_output=True, text=True)
    if result.returncode == 0:
        print("[✓] SWAN run completed successfully.")
    else:
        print("[!] SWAN run failed:")
        print(result.stderr)

def main():
    # === Replace with your actual data filenames ===
    wind_file = "wind.txt"            # Format: lon, lat, u, v or compatible with SWAN
    bathymetry_file = "bathymetry.txt"     # Format: lon, lat, depth

    swan_input_filename = create_swan_input_file(wind_file, bathymetry_file)
    run_swan(swan_input_filename)

if __name__ == "__main__":
    main()
