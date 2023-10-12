# Description 

# FastApi Crud 
Installation steps:
1. Create a python virtual environement
- for a windows machine use the following:
```
python -m venv venv
```
- for a linux machine use the following:
```
python3 -m venv venv
```
2. Activate the virutal environment 
- for a windows machine use the following:
```
venv\Scripts\activate 
```
- for a linux machine use the following:
```
source venv/bin/activate
```
3. install dependencies 
```
pip install -r requirements.txt
```
4. run the uvicorn server 
```
uvicorn main:app
```
5. You can acess the app routes documentation on 
```
http://localhoste:8000/docs
```