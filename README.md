# support-api
> This is the API for the Iterview Take home Assignment. 

This utilizes a SMTP server and a fake email to send the free coupon found in templates and an a MongoDB cloud instance in order to store 
and serve user submission data. I wanted to send over a Docker container but the Flask routine kept failing on installs. 


## Usage (Mac + Linux)
```python
git clone...
cd support-api
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python app.py
curl http://localhost:5000/send-mail
```

## Usage (Mac)
```python
git clone...
cd support-api
virtualenv env
source env/Scripts/activate
pip install -r requirements.txt
python app.py
curl http://localhost:5000/
```
After this you can run the React Application