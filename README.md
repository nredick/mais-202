# Stone Classifier 
Final project created for McGill AI Society: Accelerated Introduction to Machine Learning (Winter 2020).

Training and test datasets created specifically for this project via webscraping and sourced from the Smithsonian NMNH Geology Collections Data Portal [https://geogallery.si.edu/portal] (educational use only). 

## Project Description

The stone classifier project is a webapp that classifies images of stones into four categories (rock, fossil, gemstone, mineral). The dataset was created by scraping and parsing the NMNH Geology Collections Data Portal with BeautifulSoup. Image preprocessing included removal of duplicates, resizing, Gaussian blur to reduce noise. I built the model using Keras/Tensorflow on Google Colab, utilizing a convolutional neural network (CNN). The stone-classifier-webapp backend is based on the Flask module. 

## Deploying the Webapp

The webapp runs locally from the terminal or command line. 

To utilize the webapp, clone the repository to your local machine. Install all packages from requirements.txt. 
>The app requires Tensorflow, which utilizes Python 3.5-3.7 and can be run easily within a pipenv shell. 

Navigate to the 'stone-classifier-webapp' directory and run the command 
```
python app.py
```

The app is hosted at [http://127.0.0.1:5000/]

*The 'Stone Classifier' webapp is based on:
[https://github.com/mtobeiyf/keras-flask-deploy-webapp/blob/master/app.py]*

## Repository Organization

This repository contains the scripts used to webscrape and create the datasets, preprocess and label the original images, train the model, and build the webapp. 

mais202
|
├── README.md
├── deliverables/
│   ├── Data Selection Proposal.pdf
│   ├── Final Training Results & Demonstration Proposal.pdf
│   └── Progress and Preliminary Results.pdf
|	* contains final project deliverables and proposals for the MAIS 202 course 
├── model/
│   └── mais_final_project.py/
|	* Python script written on Google Colab to build the CNN
├── stone-classifier-webapp
│   ├── Dockerfile
│   ├── LICENSE
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── app.py
│   ├── models/
│   │   ├── model.h5
│   │   └── model.json
|   |	    * final CNN model 	
│   ├── requirements.txt
│   ├── static/
│   │   ├── classes.csv
│   │   ├── main.css
│   │   └── main.js
|   |	    * CSS and JS scripts for the landing page 
│   ├── templates/
│   │   ├── base.html
│   │   └── index.html
|   |	    * HTML for landing page 
│   └── util.py
└── webscraping/
    ├── DataCollection/
    │   ├── GatherData/
    │   │   ├── class_sort.py
    │   │   ├── get_html.py
    │   │   ├── get_images.py
    │   │   ├── get_names.py
    │   │   ├── parser.py
    │   │   └── pipeline.py
    |	|	* methods used to send GET requests for image data, parse HTML responses            
    |	|	using Beautiful Soup, retrieve labels for each image 
    │   └── Preprocess/
    │       └── partition.py
    |		* python script to sort images into 4 distinct
    |   	classes, resize images and remove duplicate images
    └── requirements.txt

