# Xtractor  
This project contains various files and modules that enable the user to extract content that is relevant to them from Unstructured Data.  
The first is a CLI implementation to extract data and match them to the corresponding context provided by the user.  
  

A web application for the same has been implemented using Django, that also includes features like keyword-filtering, graphic interface for finding the necessary piece of information, etc.  

The img2table module uses Digital Image Processing techniques using OpenCV that is a specific application of what tools like OCR-reader and Pytesseract do.  
  
The other modules deal with identifying morphology of the unstructured document and format conversion.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites and Installation

It is recommended that these steps be done in a virtual environment.  
  
Clone the repository to your local machine.  

```
git clone https://github.com/bhattsahil1/smart-xtractor
```

Run the following command to install all the necessary packages.

```
pip3 install -r requirements.txt
```

### Running Xtractor locally

#### For the CLI implementation, run the following:  
```
cd src/  
python3 pdfread.py <filepath>
```
The outputs can be observed in the corresponding directories for text, images and tables.  

#### For local deployment of the Django application:
1. Navigate to the directory 'xtractor':  
```
cd xtractor/  
```

2. Make the necessary migrations  
```
python3 manage.py migrate
```
3. Deploy it locally  and navigate to localhost
```
python3 manage.py runserver
```
#### Tabular data extraction from scanned images:  
```
cd src/  
python3 scanned_extract.py <filepath>  
```
The output will be stored in the same directory as a csv file.  
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
