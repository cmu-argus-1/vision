# README

## Data Selection for different conditions, e.g. cloud coverage & time

1. **Random Selection**: Start by randomly picking a subset of images from your dataset.

2. **Stratify by Cloud Cover**: Divide the selected images into groups based on cloud cover percentages (e.g., 0-10%, 11-20%).

3. **Proportional Sampling**: Within each cloud cover group, sample images proportionally to match the original cloud cover distribution.

4. **Verification & Testing**: Start with the proposed selection of the dataset, use validation data to update the selection

## Data Augmentation

1. **Resize**: We resize the image to certain resoltuion, but this may cause distortion problems. (How to make sure the images are similar to the real ones?)
   
2. **Augment**:  We apply several methods to do data augmentation. (TODO: Confirm the methods and add more methods)
   1. **Brightness**: We change the brightness of the image.
   2. **Contrast**: We change the contrast of the image.
   3. **Rotation**: We rotate the image. (TODO: rotate has issues handling the borders of the image after rotation)