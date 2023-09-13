**Setting up the backend service**

To setup the backend service, begin by installing the virutal environment in the `bakcend` folder:

```
pip install virtualenv
virtualenv venv --python=python3.9
```
To activate the virtual environment (macOS), execute the following command:
```
source ./venv/bin/activate
```

Install the necessary packages by either executing `pip install -r requirements.txt` or the following commands:
```
pip install Flask
pip install Flask-RESTful
pip install Flask-JWT
pip install -U flask-cors
pip install langchain
pip install flask_caching
pip install pypdf
pip install openai
pip install "unstructured[all-docs]"
pip install tiktoken
```


**OpenAI**