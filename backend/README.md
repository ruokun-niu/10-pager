**Setting up the backend service**
```
virtualenv venv --python=python3.9
source ./venv/bin/activate
pip install Flask
pip install Flask-RESTful
pip install Flask-JWT
pip install -U flask-cors
pip install langchain
pip install flask_caching
pip install pypdf
pip install openai
pip install "unstructured[all-docs]"
pip install chromadb
pip install tiktoken

OR `pip install -r requirements.txt`
```

**OpenAI**