from pathlib import Path

import pandas as pd


CSV_PATH = Path(
    "data/seeds/standards_master_phase1.csv"
)


missing_standards = [
    {
        "is_number": "IS 12269:2013",
        "title": "Ordinary Portland Cement 53 Grade - Specification",
        "domain": "Civil Engineering / Cement",
        "standard_type": "Product Specification",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source verified",
        "status": "Historical/Referenced Version",
        "embedding_text": "IS 12269:2013 | Ordinary Portland Cement 53 Grade - Specification | Civil Engineering / Cement | Product Specification",
        "source_document": "BIS official certification document",
        "source_url": "https://www.bis.gov.in/qazwsx/cmd/GS-STI_12269_27082014.pdf",
        "reviewed_in": None,
        "amendment_count": 1,
        "certification_status": "Mandatory Certification",
        "supersedes": "IS 12269:1987",
        "superseded_by": None,
        "metadata_rule": "Referenced historical version; current-version resolution to be handled separately."
    },

    {
        "is_number": "IS 3812 (Part 1):2013",
        "title": "Pulverized fuel ash - Specification: Part 1 For use as pozzolana in cement, cement mortar and concrete",
        "domain": "Civil Engineering / Cement",
        "standard_type": "Product Specification",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source verified",
        "status": "Active/Referenced",
        "embedding_text": "IS 3812 (Part 1):2013 | Pulverized fuel ash - Specification | Civil Engineering / Cement | Product Specification",
        "source_document": "BIS LIMS / BIS cement standards",
        "source_url": "https://lims.bis.gov.in/home/search_is_number/?is_number__doc_no=3812",
        "reviewed_in": None,
        "amendment_count": None,
        "certification_status": None,
        "supersedes": None,
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },

    {
        "is_number": "IS 12089:1987",
        "title": "Specification for granulated slag for the manufacture of Portland slag cement",
        "domain": "Civil Engineering / Cement",
        "standard_type": "Product Specification",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source verified",
        "status": "Referenced",
        "embedding_text": "IS 12089:1987 | Granulated slag for manufacture of Portland slag cement | Civil Engineering / Cement | Product Specification",
        "source_document": "BIS LIMS",
        "source_url": "https://lims.bis.gov.in/home/search_is_number/?is_number__doc_no=12089",
        "reviewed_in": None,
        "amendment_count": None,
        "certification_status": None,
        "supersedes": None,
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },

    {
        "is_number": "IS 15388:2003",
        "title": "Silica Fume - Specification",
        "domain": "Civil Engineering / Cement",
        "standard_type": "Product Specification",
        "source_authority": "BIS",
        "source_type": "BIS official standard",
        "verification_status": "BIS-source verified",
        "status": "Active/Referenced",
        "embedding_text": "IS 15388:2003 | Silica Fume - Specification | Civil Engineering / Cement | Product Specification",
        "source_document": "BIS Standard Details",
        "source_url": "https://standards.bis.gov.in/website/standard-details",
        "reviewed_in": "2022",
        "amendment_count": 1,
        "certification_status": "Voluntary Certification",
        "supersedes": None,
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },

    {
        "is_number": "IS 1760 (Part 3):1992",
        "title": "Chemical Analysis of Limestone, Dolomite and Allied Materials - Part 3 Determination of Iron Oxide, Alumina, Calcium Oxide and Magnesia",
        "domain": "Civil Engineering / Cement",
        "standard_type": "Test Method",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source verified",
        "status": "Historical/Referenced Version",
        "embedding_text": "IS 1760 (Part 3):1992 | Chemical Analysis of Limestone, Dolomite and Allied Materials | Test Method",
        "source_document": "BIS standard / revision bulletin",
        "source_url": "https://www.services.bis.gov.in/tmp/weekly_bulletin_2_575.pdf",
        "reviewed_in": None,
        "amendment_count": None,
        "certification_status": None,
        "supersedes": None,
        "superseded_by": "IS 1760 (Part 3):2025",
        "metadata_rule": "Historical version cited by another standard; preserve for version intelligence."
    },

    {
        "is_number": "IS 1727:1967",
        "title": "Methods of Test for Pozzolanic Materials",
        "domain": "Civil Engineering / Cement",
        "standard_type": "Test Method",
        "source_authority": "BIS",
        "source_type": "BIS official standard",
        "verification_status": "BIS-source verified",
        "status": "Referenced",
        "embedding_text": "IS 1727:1967 | Methods of Test for Pozzolanic Materials | Civil Engineering / Cement | Test Method",
        "source_document": "BIS standard preview",
        "source_url": "https://www.services.bis.gov.in/tmp/SR1727.pdf",
        "reviewed_in": None,
        "amendment_count": None,
        "certification_status": None,
        "supersedes": None,
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },

    {
        "is_number": "IS 17410:2020",
        "title": "Medical Textiles - Bio-Protective Coverall - Specification",
        "domain": "Textiles / Medical Textiles",
        "standard_type": "Product Specification",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source identified",
        "status": "Referenced",
        "embedding_text": "IS 17410:2020 | Medical Textiles - Bio-Protective Coverall - Specification | Medical Textiles | Product Specification",
        "source_document": "BIS official standards programme",
        "source_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/pow_new/Pow/download_pow_pdf_dept_commtt/71/134/",
        "reviewed_in": None,
        "amendment_count": None,
        "certification_status": None,
        "supersedes": None,
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },

    {
        "is_number": "IS 228 (Part 1):1987",
        "title": "Methods for Chemical Analysis of Steels - Part 1 Determination of Carbon by Volumetric Method",
        "domain": "Metallurgical Engineering / Steel",
        "standard_type": "Test Method",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source identified",
        "status": "Referenced",
        "embedding_text": "IS 228 (Part 1):1987 | Methods for Chemical Analysis of Steels | Metallurgical Engineering | Test Method",
        "source_document": "BIS Standard Details",
        "source_url": "https://services.bis.gov.in/php/BIS_2.0/bisconnect/standard_review/Standard_review/Isdetails",
        "reviewed_in": None,
        "amendment_count": None,
        "certification_status": None,
        "supersedes": None,
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },

    {
        "is_number": "IS 6396:2023",
        "title": "Steels - Determination of the Depth of Decarburization",
        "domain": "Metallurgical Engineering / Steel",
        "standard_type": "Test Method",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source verified",
        "status": "Active/Referenced",
        "embedding_text": "IS 6396:2023 | Steels - Determination of the Depth of Decarburization | Metallurgical Engineering | Test Method",
        "source_document": "BIS Standard Details",
        "source_url": "https://services.bis.gov.in/php/BIS_2.0/bisconnect/standard_review/Standard_review/Isdetails",
        "reviewed_in": None,
        "amendment_count": 0,
        "certification_status": None,
        "supersedes": "IS 6396:2000",
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },

    {
        "is_number": "IS 6885 (Part 1):2020",
        "title": "Metallic Materials - Knoop Hardness Test Part 1 Test Method",
        "domain": "Metallurgical Engineering / Testing",
        "standard_type": "Test Method",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source verified",
        "status": "Active/Referenced",
        "embedding_text": "IS 6885 (Part 1):2020 | Metallic Materials - Knoop Hardness Test Part 1 Test Method | Metallurgical Engineering | Test Method",
        "source_document": "BIS Weekly Bulletin / BIS Standard Details",
        "source_url": "https://www.services.bis.gov.in/tmp/weekly_bulletin_3_76.pdf",
        "reviewed_in": None,
        "amendment_count": None,
        "certification_status": None,
        "supersedes": None,
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },

    {
        "is_number": "IS 16354:2015",
        "title": "Metakaolin for use in cement, cement mortar and concrete - Specification",
        "domain": "Civil Engineering / Cement",
        "standard_type": "Product Specification",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source verified",
        "status": "Referenced",
        "embedding_text": "IS 16354:2015 | Metakaolin for use in cement, cement mortar and concrete - Specification | Civil Engineering / Cement | Product Specification",
        "source_document": "BIS Civil Engineering standards material",
        "source_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/pow_new/Pow/download_pow_pdf_dept_commtt/63/190/",
        "reviewed_in": None,
        "amendment_count": None,
        "certification_status": None,
        "supersedes": None,
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },
        {
        "is_number": "IS 9550:2024",
        "title": "Bright Steel Bars - Specification",
        "domain": "Metallurgical Engineering / Steel",
        "standard_type": "Product Specification",
        "source_authority": "BIS",
        "source_type": "BIS official standard record",
        "verification_status": "BIS-source verified",
        "status": "Active/Current",
        "embedding_text": "IS 9550:2024 | Bright Steel Bars - Specification | Metallurgical Engineering / Steel | Product Specification",
        "source_document": "BIS Standard Details",
        "source_url": "https://services.bis.gov.in/php/BIS_2.0/bisconnect/standard_review/Standard_review/Isdetails?ID=MzIwMTc%3D",
        "reviewed_in": None,
        "amendment_count": 0,
        "certification_status": None,
        "supersedes": "IS 9550:2001",
        "superseded_by": None,
        "metadata_rule": "Current BIS revision; verify latest amendment and certification metadata before production recommendation."
    },
    {
    "is_number": "IS 269:2013",
    "title": "Ordinary Portland Cement, 33 Grade",
    "domain": "Civil Engineering / Cement and Concrete",
    "standard_type": "Product Specification",
    "source_authority": "BIS",
    "source_type": "BIS official standard record",
    "verification_status": "BIS-source verified",
    "status": "Historical Version / Referenced",
    "embedding_text": "IS 269:2013 | Ordinary Portland Cement, 33 Grade | Civil Engineering / Cement and Concrete | Product Specification",
    "source_document": "BIS Standard Details",
    "source_url": "https://standards.bis.gov.in/",
    "reviewed_in": None,
    "amendment_count": 0,
    "certification_status": None,
    "supersedes": None,
    "superseded_by": "IS 269:2015",
    "metadata_rule": "Historical version explicitly referenced by IS 456:2000; preserve exact version for relationship and version-intelligence processing."
},

    {
        "is_number": "IS 1344:1981",
        "title": "Specification for Calcined Clay Pozzolana",
        "domain": "Civil Engineering / Cement",
        "standard_type": "Product Specification",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source verified",
        "status": "Referenced",
        "embedding_text": "IS 1344:1981 | Specification for Calcined Clay Pozzolana | Civil Engineering / Cement | Product Specification",
        "source_document": "BIS Civil Engineering standards material",
        "source_url": "https://www.services.bis.gov.in/tmp/WCCED21426776_10022025_1.pdf",
        "reviewed_in": None,
        "amendment_count": None,
        "certification_status": None,
        "supersedes": None,
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },

    {
        "is_number": "IS 16714:2018",
        "title": "Ground Granulated Blast Furnace Slag for Use in Cement, Mortar and Concrete - Specification",
        "domain": "Civil Engineering / Cement",
        "standard_type": "Product Specification",
        "source_authority": "BIS",
        "source_type": "BIS official source",
        "verification_status": "BIS-source verified",
        "status": "Referenced",
        "embedding_text": "IS 16714:2018 | Ground Granulated Blast Furnace Slag for Use in Cement, Mortar and Concrete - Specification | Civil Engineering / Cement | Product Specification",
        "source_document": "BIS LIMS / BIS official source",
        "source_url": "https://lims.bis.gov.in/home/search_is_number/?is_number__doc_no=16714",
        "reviewed_in": None,
        "amendment_count": None,
        "certification_status": None,
        "supersedes": None,
        "superseded_by": None,
        "metadata_rule": "Verify current lifecycle metadata from BIS Know Your Standard."
    },
]


def main():

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"CSV not found: {CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    existing_numbers = set(
        df["is_number"].astype(str).str.strip()
    )

    new_records = []

    for standard in missing_standards:

        if standard["is_number"] in existing_numbers:
            print(
                f"Already exists: "
                f"{standard['is_number']}"
            )
            continue

        new_records.append(standard)

    if not new_records:
        print("No new standards to add.")
        return

    new_df = pd.DataFrame(new_records)

    df = pd.concat(
        [df, new_df],
        ignore_index=True
    )

    df.to_csv(
        CSV_PATH,
        index=False
    )

    print(
        f"Added {len(new_records)} standards."
    )

    print(
        f"New total in CSV: {len(df)}"
    )


if __name__ == "__main__":
    main()