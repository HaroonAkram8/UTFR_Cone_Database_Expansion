# UTFR_Cone_Database_Expansion

The purpose of this project is to make up for the class imbalance in our training for YOLOv7. There are four classes that YOLOv7 is attempting to identify: blue cones, yellow cones, small orange cones, and large orange cones.

Currently, we have over 5000 labelled blue cones and yellow cones respectively. However, there are only ~500 labelled small orange cones and large orange cones for each. As a result, based on research, we found that we can "trick" YOLO into detecting more cones by creating fake images of cones on various background (i.e. empty parking lots, airports, skate parks, etc.). The program effectively copy-pastes the inputted image onto the inputted background image to create fake images to artificially expand our database. The program will do things like scaling based on distance, however, it is very much background image dependent (different camera angles may lead to inconsistent results). Overall, this is acceptable for our purposes.

The program will output images with a coco.json files that can be imported to Roboflow to automatically label the images.

There are several important input parameters to the copy_paste_images() function:

background_path: path to the background images (i.e. an empty parking lot).
foreground_path: path to the image you want to copy-paste on top the background (i.e. the cone).
output_path: path to where you want the output to be.
num_images_to_generate: number of output images you want to create (recommend 15-50 for best results).
min_per_image: minimum number of foreground images you want in each background images (i.e. you may want at least 4 cones per image).
max_per_image: maximum number of foreground images you want in each background images (i.e. you may want at most 8 per image).
percent_height_generation_limit: the max limit for where the foreground images will appear (i.e. you only want cones to appear in the bottom 80% of the background images  (since the top 20% is only the sky as an example) so you input 80 here).
category_id: the class category for YOLO and Roboflow (i.e. "large_orange_cone", "small_orange_cone", "blue_cone", "yellow_cone").
coco_dict: the generated coco dictionary from the function set_up_coco_dict().
size_mult: A size multiplier to manually adjust how much you want the foreground images to be scaled in the output (dependent on the input images).

This project is still work-in-progress. It requires code clean up, revision and to be improved upon in terms of the image generation.
