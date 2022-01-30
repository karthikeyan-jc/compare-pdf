# COMPARE-PDF

A Flask driven restful API for comparing two PDF files.

## Description

This project contains a POST endpoint (../compare) which takes in two PDF files as form-data input and returns a pdf which contains a side by side comparison of each page in the input PDFs.

## Installation / Usage
* If you wish to run your own build, first ensure you have python3 globally installed in your computer.
* After this, ensure you have installed virtualenv globally as well. If not, run this:

    ```bash
    pip install virtualenv
    ```

* Git clone this repo

    ```bash
    git clone https://github.com/karthikeyan-jc/compare-pdf.git
    ```
* cd into your the cloned repo
    ```bash
    cd compare-pdf
    ```
* Create and activate your virtual environment:

    ```bash
    virtualenv -p python3 venv
    source venv/bin/activate
    ```
* Install your requirements
  
    ```bash
    (venv)$ pip install -r requirements.txt
    ```
* Running the Server

    On your terminal, run the server using this one simple command:

    ```bash
    (venv)$ flask run
    ```
* You can now test the endpoint from Postman or anyother API platform by sending a POST request to http://127.0.0.1:5000/compare with the two pdf files as 'f1', 'f2' form-data.
