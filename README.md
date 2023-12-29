# IPTC metadata
Add metadata to JPGs using IPTCInfo3. Created to support image processing at Letterform Archive in San Francisco, CA. 

## How It Works
This is a python script to add csv metadata to JPG files for easier access. The fields pulled from csv sheets are:

- title
- date
- earliestDate
- agent: name: person
- agent: name: organization
- measurements
- location: creation

These are all being dumped into the `keywords` IPTC field as it is an easy non-hierarchical, non-controlled vocab field. The one exception is `location: creation` which is split and the country is also added to the `country` IPTC field. The script also acknowledges blank fields in the csv (e.g. `[no title]`).

The files are matched to the csv by the `work ID`, which is the unique identifier assigned to the object by Letterform Archive. It is in the format: `lfa_collectionName_XXXX`, where the X's are digits. The corresponding image files are `lfa_collectionName_XXXX_XXX`, where the last 3 digits count the image number per object. For example, the last image of an object that has 4-sides would be `lfa_collectionName_XXXX_004`. Any unique identifier can be substituted. 

### Functions
This script has 3 functions: 
**load_csv_data(csv_path)**: Loads csv data into dictionary for easy access. Returns: csv header (list of str), csv data (dict). 

**add_iptc_metadata(image_path, metadata)**: Extracts requested metadata and saves to image file.

**process_csv_row(work_id, images_dir, header)**: Processes each row of csv that matches images in directory by calling `add_iptc_metadata()`. 

### Driver
This code runs when the script is being run as the main program (not imported as module). It prompts the user to input the path of a folder containing images and the csv file path, handling potential issues such as trailing/leading spaces, backslashes and spaces. For each work_id in the csv data, it identifies matching image files based on the work ID and calls `process_csv_row()`

## Usage (Mac) 
1. Download most recent version of [IPTCInfo3](https://github.com/james-see/iptcinfo3/blob/master/iptcinfo3.py) directly from Github (not pypi) and store in appropriate folder. For example, I use anaconda so replaced the previous `iptcinfo3.py` file in `anaconda3/lib/python3.11/site-packages/iptcinfo3.py` with the version linked above.   
3. Separate images to process into their own directory.
4. Run the following command in terminal:

       $ python3 path/to/iptc_metadata.py

5. When prompted, drag the **folder** of images to be processed into terminal to copy the path and press `return`.

        Add images folder path: /path/to/images/to/be/processed/

6. When prompted, drag the corresponding metadata **csv file** into terminal to copy the path and press `return`.

         Add CSV file path: /path/to/metadata.csv

Images will now be processed. Terminal output will provide updates about processing status and/or error messages if issues exist. 

### Notes on IPTC Metadata 
As written, metadata will be stored in the `keywords` and `country` IPTC fields. To view the metadata, locate those assigned fields in a viewer such as Adobe Bridge. For example: 

<img width="1118" alt="metadata-example" src="https://github.com/elliswmartin/iptc-metadata/assets/54450015/c13d44d8-7aca-4bd1-b5b9-41a2a9713ef5">

Consult the [IPTC Photo Metadata User Guide](https://www.iptc.org/std/photometadata/documentation/userguide/) and IPTCInfo3 documentation to map to different fields.  


