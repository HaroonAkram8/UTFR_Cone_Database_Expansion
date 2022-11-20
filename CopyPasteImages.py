from PIL import Image, ImageDraw, ImageFilter
import random
import math
import json
from datetime import datetime

# Constants
LARGE_ORANGE = 2
SMALL_ORANGE = 3

# Add a foreground image to a background image between min_per_image and max_per_image times.
def copy_paste_images(background_path, foreground_path, output_path, num_images_to_generate, min_per_image, max_per_image, percent_height_generation_limit, category_id, coco_dict, size_mult):
    im1 = Image.open(background_path)
    im2 = Image.open(foreground_path)

    im1_width, im1_height = im1.size
    
    images_list = []
    annotations_list = []
    annotation_id = 0
    
    # Create num_images_to_generate images with the input background and foreground images
    for image_num in range(num_images_to_generate):
        back_im = im1.copy()
        boxes = []
        
        # Choose a random number of cones to add to the image between min and max specified in the input parameters
        num_added_to_pic = random.randint(min_per_image, max_per_image)
        
        for paste_num in range(num_added_to_pic):
            # Get the y-position of the image as a random number between the height specified in the input parameter to 80% of the max height of the image
            y_pos = random.randint(im1_height * (100 - percent_height_generation_limit) // 100, im1_height * 80 // 100)
            x_pos = random.randint(0, im1_width // 100) * 90
            
            # resize the image to y_pos / 2.5
            resize = int(y_pos / 2.5 * size_mult)
            
            # Create a copy of foreground image and resize it
            im3 = im2.copy()
            im3.thumbnail((resize, resize), Image.Resampling.LANCZOS)
            
            im3_width, im3_height = im3.size
            
            # The purpose here is to ensure two cones do not overlap in a way that would be impossible (i.e. a cone
            # that is farther away from another cone appears to be in front of it)
            restart = True
            while restart:
                restart = False
                # Check each cone against this new cone to ensure the unwanted overlap does not occur
                for box in boxes:
                    # The puspose of thes if statements is to check to see if the unwanted overlap we discussed above affects the current cone
                    if y_pos <= box.get('y'):
                        if y_pos + im3_height >= box.get('y') and y_pos + im3_height <= box.get('y') + box.get('height'):
                            if x_pos >= box.get('x') and x_pos <= box.get('x') + box.get('height') or x_pos + im3_width >= box.get('x') and x_pos + im3_width <= box.get('x') + box.get('height'):
                                # Get new x and y positions
                                y_pos = random.randint(im1_height * (100 - percent_height_generation_limit) // 100, im1_height * 80 // 100)
                                x_pos = random.randint(0, im1_width // 100) * 90
                                
                                # Get the new size of the image from the new y position
                                resize = int(y_pos / 2.5 * size_mult)
                                im3 = im2.copy()
                                im3.thumbnail((resize, resize), Image.Resampling.LANCZOS)
                                im3_width, im3_height = im3.size
                                
                                # If we found an unwanted overlap we have to check all the cones from the beginning with out new x and y positions to ensure
                                # these new positions do not have the any new unwanted overlaps.
                                restart = True
                                break
            
            # Add the resized image to the background at a random x-position and to the precalculated random y-position. The last parameter is to ensure transparency.
            back_im.paste(im3, (x_pos, y_pos), im3)
            
            # Add image data to boxes list
            dict_box = {"x": x_pos,
                        "y": y_pos,
                        "width": im3_width,
                        "height": im3_height}
            
            boxes.append(dict_box)
            annotation = {"id": annotation_id, "image_id": image_num, "category_id": category_id, "bbox": [dict_box["x"], dict_box["y"], dict_box["width"], dict_box["height"]],
                          "area": dict_box["width"] * dict_box["height"], "segmentation": [], "iscrowd": 0}
            annotations_list.append(annotation)
            annotation_id += 1
        
        # Save the image to the specified path
        output_image_name = 'output_image_' + str(image_num) + '.png'
        back_im.save(output_path + output_image_name, quality=95)
        
        # Add image to dictionary
        image_dict = {"id": image_num, "license": 1, "file_name": output_image_name, "height": im1_height, "width": im1_width, "date_captured": datetime.today().strftime('%Y/%m/%d')}
        images_list.append(image_dict)
    
    coco_dict["images"] = images_list
    coco_dict["annotations"] = annotations_list
    
    # Write to a new json file
    with open(output_path + '_annotations.coco.json', "w") as outfile:
        outfile.write(json.dumps(coco_dict))

def set_up_coco_dict():
    set_up_dict = {"info": {}, "licenses": [], "categories": [], "images": [], "annotations": [], "segment_info": []}
    
    set_up_dict["info"] = {"description": "Copy Paste program generated images.", "url": "", "version": "1.0", "year": datetime.today().strftime('%Y'), "contributor": "Haroon (⌐■_■)", "date_created": datetime.today().strftime('%Y/%m/%d')}
    set_up_dict["licenses"] = [{"id": 1, "url": "", "name": "TEST"}]
    set_up_dict["categories"] = [{"id": 0, "name": "Cones", "supercategory": "none"},
                                 {"id": 1, "name": "blue", "supercategory": "Cones"},
                                 {"id": 2, "name": "large_orange", "supercategory": "Cones"},
                                 {"id": 3, "name": "small_orange", "supercategory": "Cones"},
                                 {"id": 4, "name": "yellow", "supercategory": "Cones"}]
                                 
    return set_up_dict

# Main starts here
coco_dict = set_up_coco_dict()

background_path = 'Parking_Lot_Images\\parking_lot_14.png'
foreground_path = 'Cone_Images\\small_orange_cone.png'
output_path = 'Output_Images\\Small_Orange\\Test14\\'

copy_paste_images(background_path, foreground_path, output_path, 50, 5, 10, 50, SMALL_ORANGE, coco_dict, 0.5)