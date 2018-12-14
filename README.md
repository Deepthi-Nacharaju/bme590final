# bme590final Image Processor
#### Haeryn Kim, Deepthi Nacharaju, Ashish Venkara

##### Front End User Interface

###### Patient ID
Must contain an ID value before image will be processed

###### Original Image
Can be opened and cleared. Histogram describing color intensities is located directly below the original image window. If this image space is clear, the processing function buttons will open an error window warning the user to open an image first. The Image's size is displayed beneath the open and clear buttons once the file is opened.

###### Processing Buttons
Uses `/new_image` POST request to run processing on virtual machine server. Completed GET request to update count values and displays these values at the bottom right of the screen. Current time stamp and how long it takes to process the image is printed underneath the Notes text box.
  * Histogram Equalization:
    * WRITE THINGS HERE
  * Contrast Switch:
    * WRITE THINGS HERE
  * Log compression:
    * WRITE THINGS HERE
  * Reverse video
    * WRITE THINGS HERE

###### Notes
Any provided notes are optional but will be uploaded and stored with the processed image.

##### Save buttons
Will save the processed image to a chosen location on the users machine as either a JPG, PNG, or compressed TIFF file(s)

###### Server Status
Any action that requires a POST or GET request will post an update to this window to notify the user of the status of the request.

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
  * dictionary with count values for histogram equalization, contrast stretching, log compression, and reverse video
    * `r['histogram_count']`
    * `r['contrast_count']`
    * `r['log_count']`
    * `r['reverse_count']`

* `/data/all/<patient_id>`
  * dictionary with all fields in ImageDB class available on server
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
