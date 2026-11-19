from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================
BASE_DIR = "/nfs/grad/directory_mockup/data"

STATIONS = ["tbl", "bnd"]
YEARS = ["2023", "2024"]

# Define the sub-formats for L1b
L1B_FORMATS = ["netcdf", "bsrn", "surfrad"]

# Define the products for L2
L2_PRODUCTS = ["AOD", "RadFlux", "QC_Rad"]

# Define the output products for L3
L3_PRODUCTS = ["Monthly_Climatology", "Yearly_Climatology"]

# Define categories for L4 (Placeholder)
L4_CATEGORIES = ["internal", "external"]

# ==========================================
# README DEFINITIONS
# ==========================================
LEVEL_READMES = {
    "L0_raw": """# Level 0: Raw Data
**Definition:** Unprocessed, high-frequency electrical signals recorded directly from the ground sensors (e.g., millivolts, resistance). Data is immutable and serves as the absolute baseline.
**Hierarchy:** `L0_raw / [Station] / [Year]`
*No archive folder is used here because raw data is never versioned or overwritten.*
""",
    "L1a_calibrated": """# Level 1a: Calibrated Data
**Definition:** Raw signals from L0 converted into physical radiometric units (W/m²). Instrument-specific calibration coefficients and temperature dependencies have been applied.
**Hierarchy:** `L1a_calibrated / [Station] / [Year]`
""",
    "L1b_qced": """# Level 1b: Quality-Controlled (QCed) Data
**Definition:** Calibrated data from L1a that has been passed through automated quality control algorithms. Values are flagged for physical limits and closure tests. The output is sorted by specific file formats required for downstream ingestion.
**Hierarchy:** `L1b_qced / [Station] / [Format] / [Year]`
**Formats:** NetCDF, BSRN ASCII, SURFRAD ASCII
""",
    "L2_post_qc": """# Level 2: Post-Processing & Value-Added Products
**Definition:** Derived physical products calculated from the QCed Level 1b datastreams. This includes specialized post-processing algorithms like Aerosol Optical Depth (AOD) and advanced Radiative Flux (RadFlux) modeling.
**Hierarchy:** `L2_post_qc / [Station] / [Product] / [Year]`
""",
    "L3_products": """# Level 3: Finalized Data Products
**Definition:** Highly processed, gap-filled, and temporally aggregated datasets intended for end-users, modelers, and climatological studies. 
**Hierarchy:** `L3_products / [Product] / [Station]`
*Note: The hierarchy flips at this level to group data primarily by the climatological product rather than the station.*
""",
    "L4_models": """# Level 4: Model & External Model Data
**Definition:** An operational placeholder for data output from internal predictive models, machine learning applications, and ingestion of external datasets (e.g., NWP forecasts, satellite reanalysis).
**Hierarchy:** `L4_models / [Category] / [Station] / [Year]`
*Note: This level is currently a placeholder for future development.*
""",
}


# ==========================================
# GENERATION LOGIC
# ==========================================
def build_skeleton():
    paths_to_create = []

    for station in STATIONS:
        # L3 Products (Hierarchy: Level -> Product -> Station)
        for product in L3_PRODUCTS:
            paths_to_create.append(f"L3_products/{product}/{station}/.archive")

        for year in YEARS:
            # L0 Raw (No archive folder needed for raw data)
            paths_to_create.append(f"L0_raw/{station}/{year}")

            # L1a Calibrated
            paths_to_create.append(f"L1a_calibrated/{station}/{year}/.archive")

            # L1b QCed (Hierarchy includes format)
            for fmt in L1B_FORMATS:
                paths_to_create.append(f"L1b_qced/{station}/{fmt}/{year}/.archive")

            # L2 Post-QC
            for l2_prod in L2_PRODUCTS:
                paths_to_create.append(
                    f"L2_post_qc/{station}/{l2_prod}/{year}/.archive"
                )

            # L4 Models (Placeholder)
            for l4_cat in L4_CATEGORIES:
                paths_to_create.append(f"L4_models/{l4_cat}/{station}/{year}/.archive")

    # Execute directory creation
    for relative_path in paths_to_create:
        full_path = Path(BASE_DIR) / relative_path

        # exist_ok=True ensures it won't crash if the folder already exists
        full_path.mkdir(parents=True, exist_ok=True)

        # Initialize a changelog file next to the .archive folders
        if ".archive" in full_path.parts:
            # The parent of the .archive folder is the active data directory
            changelog_path = full_path.parent / "changelog.csv"
            if not changelog_path.exists():
                with open(changelog_path, "w") as f:
                    f.write("Date,Filename,Version,Change_Description\n")

    # Execute README creation
    for level, readme_content in LEVEL_READMES.items():
        readme_path = Path(BASE_DIR) / level / "README.md"
        # Only write the README if it doesn't already exist to prevent overwriting manual edits
        if not readme_path.exists():
            with open(readme_path, "w") as f:
                f.write(readme_content)
            print(f"Created README: {readme_path}")


if __name__ == "__main__":
    print(f"Initializing directory skeleton at: {BASE_DIR}...\n")
    build_skeleton()
    print("\nSkeleton generation complete.")
