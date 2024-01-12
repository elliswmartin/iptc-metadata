import os, csv
from iptcinfo3 import IPTCInfo
from collections import Counter

'''

TODO: add error handling for space in folder name
TODO: test long description behavior 
TODO: test csv from google sheet w/ multiple sheets ??? 
TODO: Improve brittleness so does not fail but instead reports errors and continues processing. 
TODO: suppress char warning    https://stackoverflow.com/questions/50407738/python-disable-iptcinfo-warning
TODO: success/fail Counter() at end 
TODO: Update documentation once get through most/all of the above
'''

''' 
IPTCInfo3 available fields: 'object name', 'edit status', 'editorial update', 'urgency', 'subject reference', 'category', 'supplemental category', 'fixture identifier', 'keywords', 'content location code', 'content location name', 'release date', 'release time', 'expiration date', 'expiration time', 'special instructions', 'action advised', 'reference service', 'reference date', 'reference number', 'date created', 'time created', 'digital creation date', 'digital creation time', 'originating program', 'program version', 'object cycle', 'by-line', 'by-line title', 'city', 'sub-location', 'province/state', 'country/primary location code', 'country/primary location name', 'original transmission reference', 'headline', 'credit', 'source', 'copyright notice', 'contact', 'caption/abstract', 'local caption', 'writer/editor', 'image type', 'image orientation', 'language identifier','custom1', 'custom2', 'custom3', 'custom4', 'custom5', 'custom6', 'custom7', 'custom8', 'custom9', 'custom10', 'custom11', 'custom12', 'custom13', 'custom14', 'custom15', 'custom16', 'custom17', 'custom18', 'custom19', 'custom20']
'''


''' 
PUB DIGI::::

CHANGE VIEW SO CAN SEE IPTC(IIM, legacy): https://helpx.adobe.com/bridge/using/metadata-adobe-bridge.html

Notes: 
Creator: Any info in Agent: name: person added to Author
Creator: Any info in Agent: name: organization added to Author Title  
Title: We don't currently have any workflow in place to note official (descriptive titles are handled the same as official)
Vol/Issue: We catalog to include volume, issue, month, or other relevant periodical info in title if applicable & available. 
Dims (in): Converts measurements in cm to in 
Medium: Added material and technique fields to Headline. 

Questions: 
Prefer list of creators or keywords? Or can pull 2-3 specific ones (based on word e.g. "designer" into fields)
Do you do dims width x height or height x width? 
Do you want stylePeriod or workType?
'''



''' 
FUNCTIONS
'''
# Load csv data into dictionary for easy access
def load_csv_data(csv_path):
    csv_data = {}
    with open(csv_path, newline='') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        for row in reader:
            work_id = row[header.index('work: id')].lower()
            csv_data[work_id] = row
    return header, csv_data

# Extract requested metadata and save to image file
def add_iptc_metadata(image_path, metadata):
    try:
        # Open the image with iptcinfo3
        iptc_data = IPTCInfo(image_path) 

        # Check if IPTC data already exists
        if iptc_data:

            # Add Agent: Person to 'by-line' IPTC = 'Creator' Bridge
            # TODO - change this to strictly authors/designers 
            iptc_data['by-line']=metadata.get("agent: name: person") or "[no pers]"

            # Add Agent: Org to 'by-line title' IPTC = 'Creator: Job Title' Bridge
            iptc_data['by-line title']= metadata.get("agent: name: organization") or "[no org]"

            # Add Date/EarliestDate to 'headline' IPTC = 'Headline' Bridge
            iptc_data['headline']= metadata.get("date") or metadata.get("earliestDate") or "[no Date]"

            # Add Description to 'caption/abstract' IPTC = 'Description' Bridge
            iptc_data['caption/abstract']=metadata.get("description")

            # Extract values from metadata based on specific column headers
            keywords = [x.strip() for x in metadata.get("agent: name: person").split(';') + metadata.get("agent: name: organization").split(';')]

            # Add Creator Info to 'keywords' IPTC = 'Keywords' Bridge 
            iptc_data["keywords"] = keywords 

            # Add height x width dims(in) to 'writer/editor' IPTC ='Description Writer' Bridge 
            if metadata.get("measurements"):
                height, _, width, *unit = metadata.get("measurements").split(" ")
                dims_in = str(round(float(height) / 2.54, 3)) + " x " + str(round(float(width) / 2.54, 3)) + " in"
                iptc_data['writer/editor']=dims_in or "[no dims]"

            # Add height x width dims(cm) to 'special instructions' IPTC = 'Instructions' Bridge
            iptc_data['special instructions']= str(metadata.get("measurements")) or "[no Date]"

            ## Add ______ to 'sublocation' IPTC = Sublocation' Bridge  
            # iptc_data['sub-location']='Sublocation'

            # Add Location to IPTC Location fields
            loc = metadata.get("location: creation") or "[no loc]"
            if loc != "[no loc]":
                country = loc.split(':')[0].strip() 
                state = loc.split(':')[1].strip() or "[no state/prov]" 
                city = loc.split(':')[2].strip() or "[no city]"
            iptc_data["country/primary location name"] = country
            iptc_data['province/state']= state
            iptc_data['city']= city

            ## Add ________ to 'country/primary location code' IPTC ='ISO Country Code' Bridge 
            # iptc_data['country/primary location code']='ISO Country Code'

            # Add Title to 'object name' IPTC = 'Title' Bridge 
            iptc_data['object name'] = metadata.get("title") or "[no title]"
            
            # Add Material/Technique to 'original transmission reference' IPTC = 'Job Identifier' Bridge
            iptc_data['original transmission reference']=[metadata.get("material") or "[no material]", metadata.get("technique") or "[no technique]"]

            ## OTHER UNUSED WORKING FIELDS 
            # iptc_data['credit']='Credit Line'
            # iptc_data['source']='Source'
            # iptc_data['copyright notice']='Copyright Notice'

            # Save IPTC metadata
            iptc_data.save(options=["overwrite"])

            print("IPTC metadata added successfully to", image_path)

        else:
            print(f"No existing IPTC data found for {image_path}")

    except Exception as e:
        print(f"Error adding IPTC metadata to {image_path}: {e}")

# Process each row of csv based on images in directory
def process_csv_row(work_id, images_dir, header):
    img_files = [
        os.path.join(images_dir, f)
        for f in unique_img_files
        if work_id and work_id.lower() in f and f.lower().endswith(('.jpg', '.jpeg', '.tif', '.tiff'))
    ]

    metadata_list = []
    for col_name in header:
        try:
            metadata_list.append(csv_data[work_id][header.index(col_name)])
        except ValueError:
            print(f"Column '{col_name}' not found in header. Skipping row.")
            return

    # Combine metadata for all images of the same work ID
    combined_metadata = {
        col_name: metadata_list[header.index(col_name)]
        for col_name in header
    }

    for img in img_files:
        add_iptc_metadata(img, combined_metadata)

''' 
DRIVER
'''
if __name__ == "__main__":
    # User input for folder of images to process
    images_dir = "/Users/ellis/Desktop/iptc_test"
    # TODO replace -> images_dir = os.path.normpath(input("Add images folder path: ").strip().replace("\\", " ")) #.replace("/", "\\"))

    if not os.path.isdir(images_dir):
        raise FileNotFoundError("Invalid image directory")
    
    all_img_files = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.tif', '.tiff'))]
    unique_img_files = set(all_img_files)

    if not all_img_files:
        raise Exception("No valid image files found in the directory")

    # User input for csv file
    csv_path = os.path.normpath("/Users/ellis/Downloads/Emigre.csv")
    # TODO replace -> csv_path = os.path.normpath(input("Add CSV file path: ").strip().replace("\\", ""))

    try:
        header, csv_data = load_csv_data(csv_path)

        if not header:
            print("Empty CSV file")
            exit()

        for work_id in csv_data:
            matching_img_files = [f for f in unique_img_files if work_id.lower() in f]

            if matching_img_files and work_id:
                print(f"Processing CSV data for work ID: {work_id}")
                process_csv_row(work_id, images_dir, header)
  
    except csv.Error:
        print(f"File {csv_path} is not a valid CSV file")
        exit()
print("Processing complete.")