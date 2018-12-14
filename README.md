# bme590final Image Processor [1.0.0] ![alt text](https://travis-ci.org/Deepthi-Nacharaju/bme590final.svg?branch=master "Status Badge")
##### Haeryn Kim, Deepthi Nacharaju, Ashish Vankara

### Front End User Interface

###### Patient ID
Must contain an ID value before image will be processed.

###### Original Image
Can be opened and cleared. Histogram describing color intensities is located directly below the original image window. If this image space is clear, the processing function buttons will open an error window warning the user to open an image first. The Image's size is displayed beneath the open and clear buttons once the file is opened.

###### Processing Buttons
Uses `/new_image` POST request to run processing on virtual machine server. Completed GET request to update count values and displays these values at the bottom right of the screen. Current time stamp and how long it takes to process the image is printed underneath the Notes text box.
  * Histogram Equalization:
    * This function first checks if an image is grayscale and converts it if isn't. Next it performs
    histogram equalization, which maps the original image's histogram to a wider and more uniform distribution of intensity values
     such that the intensity values of the image are spread over the whole range. This allows for areas of lower local contrast to gain a higher contrast.  
  * Contrast Stretch:
    * This function performs normalization that improves the contrast in an image by stretching the range
     of intensity values it contains to span a desired range of values. It differs from histogram equalization
      by only applying a linear scaling function to the image pixel values, thereby generating less harsh enhancements. 
  * Log compression:
    * This function performs logarithmic compression that removes multiplicative gray level noise.
  * Reverse video
    * This function reverses the color scheme of each pixel, thereby generating the image's negative. 

###### Notes
Any provided notes are optional but will be uploaded and stored with the processed image.

##### Save buttons
Will save the processed image to a chosen location on the users machine as either a JPG, PNG, or compressed TIFF file(s).

###### Server Status
Any action that requires a POST or GET request will post an update to this window to notify the user of the status of the request.

### Back-end web server

##### POST Requests
* `/new_image`
  * Posted dictionary must include:
    * `r['patient_id']`
    * `r['process_id']`
      * This indicates the desired processing function to be applied to the original image. 1: Histogram Equalization, 2: Contrast Switch, 3: Log Compression, 4: Reverse Video, 0: No Processing
    * `r['image_file']`
      * Base64 Encoded image
    * `r['notes']`
      * Any notes that were provided in the Upload Notes text box. If field is empty, default string is made __No Additional Notes__
  * Saves Patient ID, process option, processed image, original image, and provided notes.


##### GET Requests
* `/`
  * returns a string that reads 'Welcome to the Image Processor!'/ This string is printed to the Server Status text box on the GUI to confirm that the server connection has been initialized.

* `/data/<patient_id>`
  * dictionary with count values for histogram equalization, contrast stretching, log compression, and reverse video.
    * `r['histogram_count']`
    * `r['contrast_count']`
    * `r['log_count']`
    * `r['reverse_count']`

* `/data/all/<patient_id>`
  * dictionary with all fields in ImageDB class available on server.
    * `r['original']`
    * `r['histogram_count']`
    * `r[contrast_count]`
    * `r[log_count]`
    * `r[reverse_count]`
    * `r['images']`
    * `r['processor']`
    * `r['images_time_stamp']`
    * `r['notes']`
* `/data/stack/<patient_id>`
  * list of all images processed for a specified patient ID
  
* `/data/last/<patient_id>`
  * Get the original image and last processed image for a specified user ID to continue processing
    * `r['original']`
    * `r['last_process]`

### Project Directory Structure
  * bme590final
    * GUI.py: Contains the script to run the graphic user interface of the image processor.
    * front_end.py: Contains the functions utilized by the GUI to perform its functions.
    * log.txt: Contains server debugging information from its most recent run.
    * requirements.txt: Specifies the dependencies of this software.
    * server.py: Contains the functions and API routes necessary for this software package.
    * test_front_end.py: Script that tests all the functions in front_end.py.
    * test_server.py: Script that tests all the functions in server.py.
    * /testing_files: Contains all the necessary files to carry out unit testing.
    
See documentation for additional details 

