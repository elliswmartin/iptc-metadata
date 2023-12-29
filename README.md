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

## Usage (Mac) 
1. Download most recent version of [IPTCInfo3](https://github.com/james-see/iptcinfo3/blob/master/iptcinfo3.py) directly from Github (not pypi) and store in appropriate folder. For example, I use anaconda so replaced the previous `iptcinfo3.py` file in `anaconda3/lib/python3.11/site-packages/iptcinfo3.py` with the version linked above.   
3. Separate images to process into their own directory.
4. Run the following command in terminal:

       $ python3 path/to/iptc_metadata.py

5. When prompted, drag the **folder** of images to be processed into terminal to copy the path and press `return`.

        Add images folder path: /path/to/images/to/be/processed/

6. When prompted, drag the corresponding metadata **csv file** into terminal to copy the path and press `return`.

         Add CSV file path: /path/to/metadata.csv

Images will now beging to process. Terminal output will provide updates about processing status and/or error messages if issues exist. 
