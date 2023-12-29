import os
import csv
from iptcinfo3 import IPTCInfo

''' 
FUNCTIONS
'''
# Add metadata to image file
def add_iptc_metadata(image_path, metadata):
    try:
        # Open the image with iptcinfo3
        iptc_data = IPTCInfo(image_path) #, force=True)

        # Check if IPTC data already exists
        if iptc_data:
            # Extract values from metadata based on specific column headers
            keywords = [
                metadata.get("title") or "[no title]",
                metadata.get("date") or "[no date]",
                metadata.get("earliestDate") or "[no earDate]",
                metadata.get("agent: name: person") or "[no pers]",
                metadata.get("agent: name: organization") or "[no org]",
                metadata.get("measurements") or "[no dims]",
                metadata.get("location: creation") 
            ]

            # Add to IPTC keywords field 
            iptc_data["keywords"] = keywords  

            # Add to IPTC country field
            loc = metadata.get("location: creation") or "[no loc]"
            if loc != "[no loc]":
                country = loc.split(':')[0] 
            iptc_data["country/primary location name"] = country

            # Save IPTC metadata
            iptc_data.save(options=["overwrite"])

            print("IPTC metadata added successfully to", image_path)

        else:
            print(f"No existing IPTC data found for {image_path}")

    except Exception as e:
        print(f"Error adding IPTC metadata to {image_path}: {e}")

# Load csv data into dictionary for easy access
def load_csv_data(csv_path):
    csv_data = {}
    with open(csv_path, newline='') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        for row in reader:
            work_id = row[header.index('work: id')]
            csv_data[work_id] = row
    return header, csv_data

# Process each row of csv based on images in directory
def process_csv_row(work_id, images_dir, header):
    img_files = [
        os.path.join(images_dir, f)
        for f in unique_img_files
        if work_id and work_id in f and f.lower().endswith(('.jpg', '.jpeg', '.tif', '.tiff'))
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
    images_dir = os.path.normpath(input("Add images folder path: ").strip().replace("\\", " ")) #.replace("/", "\\"))

    if not os.path.isdir(images_dir):
        raise FileNotFoundError("Invalid directory")
    
    all_img_files = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.tif', '.tiff'))]
    unique_img_files = set(all_img_files)

    if not all_img_files:
        raise Exception("No valid image files found in the directory")

    # User input for csv file
    csv_path = os.path.normpath(input("Add CSV file path: ").strip().replace("\\", ""))

    try:
        header, csv_data = load_csv_data(csv_path)

        if not header:
            print("Empty CSV file")
            exit()

        for work_id in csv_data:
            matching_img_files = [f for f in unique_img_files if work_id in f]

            if matching_img_files and work_id:
                print(f"Processing CSV data for work ID: {work_id}")
                process_csv_row(work_id, images_dir, header)
  
    except csv.Error:
        print(f"File {csv_path} is not a valid CSV file")
        exit()