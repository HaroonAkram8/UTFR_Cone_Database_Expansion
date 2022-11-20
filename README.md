# UTFR_Cone_Database_Expansion

The purpose of this project is to make up for the class imbalance in our training for YOLOv7. There are four classes that YOLOv7 is attempting to identify: blue cones, yellow cones, small orange cones, and large orange cones.

Currently, we have over 5000 labelled blue cones and yellow cones respectively. However, there are only ~500 labelled small orange cones and large orange cones for each. As a result, based on research, we found that we can "trick" YOLO into detecting more cones by creating fake images of cones on various background (i.e. empty parking lots, airports, ckate parks, etc.). The program effectively copy-pastes the inputted image onto the inputted background image to create fake images to artificially expand our database.

This project isstill work-in-progress. Requires code clean up, revision and to be improved upon in terms of the image generation.
