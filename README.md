# IPTC metadata
Add metadata to JPGs using IPTCInfo3. Created to support image processing at Letterform Archive (LfA) in San Francisco, CA. 

## How It Works
This is a python script to add csv metadata to JPG files for easier access. The fields pulled from LfA csv sheets are mapped onto IPTC fields, which appear with different names in various photo viewer applications (see [Notes on IPTC Metadata](#notes-on-iptc-metadata) for more). The following is the particular implementation as it appears in the Adobe Bridge IPTC (IIM, legacy) metadata section. 

| LfA field | Bridge field |
| ------------- | ------------- |
| Title | Document Title | 
| Date or EarliestDate | Headline | 
| Description | Description | 
| Measurements | Description Writer |
| Agent: Name: Person | Creator |
| Agent: Name: Org  | Creator: Job Title |
| City | City |
| State/Providence | State/Providence | 
| Country | Country | 
| Material & Technique | Transmission Reference | 
| ~ open ~ | Credit | 
| ~ open ~ | Source |
| ~ open ~ | Copyright | 

The script also acknowledges blank fields in the csv (e.g. `[no title]`).

The image files are matched to the csv by the `work ID`, which is the unique identifier assigned to the object by Letterform Archive. It is in the format: `lfa_collectionName_XXXX`, where the X's are digits. The corresponding image files are `lfa_collectionName_XXXX_XXX`, where the last 3 digits count the image number per object. For example, the last image of an object that has 4-sides would be `lfa_collectionName_XXXX_004`. Any unique identifier can be substituted. 

### Functions
This script has 3 functions: 

**load_csv_data**(csv_path): Loads csv data into dictionary for easy access. Returns: csv header (list of str), csv data (dict). 

**add_iptc_metadata**(image_path, metadata): Extracts requested metadata and saves to image file.

**process_csv_row**(work_id, images_dir, header): Processes each row of csv that matches images in directory by calling `add_iptc_metadata()`. 

### Driver
This code runs when the script is being run as the main program (not imported as module). It prompts the user to input the path of a folder containing images and the csv file path, handling potential issues such as trailing/leading spaces, backslashes and spaces. The csv is imported using `load_csv_data()`. For each work_id in the csv data, it identifies matching image files based on the work ID and calls `process_csv_row()`.

## Usage (Mac) 
0. Clone script folder to wherever you store your scripts locally by running the following command in terminal: 

       $ git clone https://github.com/elliswmartin/iptc-metadata
 
1. Download most recent version of [IPTCInfo3](https://github.com/james-see/iptcinfo3/blob/master/iptcinfo3.py) directly from Github (not pypi) and store it wherever your python libraries are stored locally. If you are unfamiliar with this process or unsure where your python libraries are stored locally, see the [IPTCInfo3 Install Help](#iptcinfo3-install-help) subsection below.  
2. Separate images to process into their own directory.
3. Run the following command in terminal:

       $ python3 path/to/iptc_metadata.py

4. When prompted, drag the **folder** of images to be processed into terminal to copy the path and press `return`.

        Add images folder path: /path/to/images/to/be/processed/

5. When prompted, drag the corresponding metadata **csv file** into terminal to copy the path and press `return`.

         Add CSV file path: /path/to/metadata.csv

Images will now be processed. Terminal output will provide updates about processing status and/or error messages if issues exist. 

### IPTCInfo3 Install Help
If you are unsure where python libraries are stored locally, I suggest installing the IPTCInfo3 library using pip, locating that file and replacing the file with the most recent version of the script. 

1. Run the following command in terminal to install IPTCInfo3 via [PyPi](https://pypi.org/project/IPTCInfo3/):

       $ pip install IPTCInfo3

2. Locate the newly installed IPTCInfo3 library by running the following command in terminal:

       $ python3 -m pip show iptcinfo3

3. From the terminal output, copy the `Location: ` file path. For example, `/opt/homebrew/lib/python3.9/site-packages` from the following output:

       Name: IPTCInfo3
       Version: ...
       Summary: ...
       Home-page: ...
       Author: ...
       Author-email: ...
       License: ...
       Location: /opt/homebrew/lib/python3.9/site-packages

4. In Finder's `Go` Menu, select `Go To Folder` and paste the copied location. 

<img width="462" alt="Screen Shot 2024-01-05 at 3 33 24 PM" src="https://github.com/elliswmartin/iptc-metadata/assets/54450015/fc316578-615b-42de-af23-5e2b435a90e5">

5. Download the most recent version of the [IPTCInfo3 script](https://github.com/james-see/iptcinfo3/blob/master/iptcinfo3.py) directly via Github.

6. Replace the original IPTCInfo3.py file downloaded via PyPi with file you just downloaded directly from Github. Return to Usage Step 2 to continue. 

### Notes on IPTC Metadata 
As written, metadata will be stored in the `keywords` and `country` IPTC fields. To view the metadata, locate those assigned fields in a viewer such as Adobe CC apps or ExifTool. For example, this is how the metadata appears in [Bridge](https://helpx.adobe.com/bridge/using/metadata-adobe-bridge.html): 

<img width="1118" alt="metadata-example" src="https://github.com/elliswmartin/iptc-metadata/assets/54450015/c13d44d8-7aca-4bd1-b5b9-41a2a9713ef5">

Consult the [IPTC Photo Metadata User Guide](https://www.iptc.org/std/photometadata/documentation/userguide/) and IPTCInfo3 documentation to map to different fields. 


