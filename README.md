# Continue context Provider local RAG
## Setup Guide Clone repository
### Create and activate your venv
Step into the cloned directory and run the following:
```
python -m venv venv 
venv\Scripts\activate
```
### Install Libraries
Under the previous directory run the following:
```
pip install "fastapi[standard]" langchain_ollama tiktoken
pip install chromadb
```
### Put your data
Under data/txt_files you can create new .txt files that contain your domain specific data to be used as context. By default, it comes with Medellin Travel data for demo purposes, but make sure to erase it.
### Populate ChromaDB Vectorial Database
Under the notebooks folder run all the chromadb-txt-processing.ipynb. This notebook will chunk the txt files and use the previously installed nomic-embed-text embedding model to generate vectorial representation of those ingested data. Finally, it populates a local ChromaDB instance.
### Start your FastApi server
Step into scripts folder and start your FastAPI Server with the following commands:
```
cd scripts
fastapi dev server.py
```
### Integrate the custom http context provider into Continue
- Open Continue .yaml settings located in %USERPROFILE%\.continue\config.yaml
- Under context insert this config pointing to your fastapi server endpoint:
```
- provider: http
    params:
        url: http://127.0.0.1:8000/retrieve
```
### Use the custom http context provider within Continue
In Continue, this HTTP provider can be used as context by typing '@' + HTTP. It should retrieve the queried most similar chunks from your data as context.