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
    
See documentation for additional details: '\bme590final\docs\build\html\index.html' 

#### Multiple Images
The branch multiple_images contains development for uploading more than one image 
to the image processor for a given patient ID. It allows the user to scroll through the images in the GUI,
but the server has issues with trying to manipulate nested lists of byte like objects. This branch can be
explored to evaluate the development of this feature, though not complete.

#### Setting up the Server
Running the following command in the terminal will initialize the server:

    FLASK_APP=server.py flask run
    
In addition, in server.py:

    __app__ == '__main__':
        connect("mongodb://bme590:Dukebm3^@ds253889.mlab.com:53889/imageprocessor")
        app.run(host="127.0.0.1")
And in GUI.py:

    server = "http://127.0.0.1:5000/"

#### Deliverables
* Robust [README.md](README.md) describing the final performance of the project.
* Tagged project code: [bme590final](https://github.com/Deepthi-Nacharaju/bme590final)
* Link to deployed web server: http://vcm-7301.vm.duke.edu:5000/
* [RFC document](https://docs.google.com/document/d/1WOm3omIRztGDvEBmDNXnpbt2n_0UI8ObQQSgk6ZhMgE/edit?usp=sharing)
* [Recorded demo](https://www.icloud.com/attachment/?u=https%3A%2F%2Fcvws.icloud-content.com%2FB%2FATUprsaV6XdVxkFuh_aGe0x4e8SdAXBS639PM4lr-pafJvteXNbrcT7_%2F%24%7Bf%7D%3Fo%3DAkGhIaF1yzmLqv50DaqFENksmCzLL5OQg2Ky4czI5tOs%26v%3D1%26x%3D3%26a%3DByeID9Xdhyfb23Js4Wf52Mnlr4frA3yCSAEACAHIAP9w7nGEA7zZRw%26e%3D1547423706%26k%3D%24%7Buk%7D%26fl%3D%26r%3D7FC3F1CC-3F42-42D0-B9C2-2D4E5CC75FE4-1%26ckc%3Dcom.apple.largeattachment%26ckz%3DDC5B2A1A-CAB7-431B-930F-6048E15AB09B%26p%3D42%26s%3DUX-7EI96Iw0J-gPCzh2JDZgSUes&uk=DiNdOS4r2HBaLWekipFbcw&f=IMG_2575.MOV&sz=686681005) of image processor in action. 

### License
MIT License

Copyright (c) 2018 Ashish Vankara, Deepthi Nacharaju, Haeryn Kim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

