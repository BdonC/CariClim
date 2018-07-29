## Warming level calculator (WLC)

### Run locally for debugging

Warming level calculator is a web application, based on python, flask, nginx and gunicorn. Data processing is based on netCDF4, numpy and dimarray. You can run this app locally for development and debugging with
```
python run.py
```

### Local testing with gunicorn

gunicorn is a resource-efficient webserver that can handle parallel requests.
Test it by starting
```
gunicorn run:app --workers 3 --worker-class gevent -b 0.0.0.0:5000
```

### Run in PIK virtual machine (currently se51)

docker seems difficult within opensuse as host. two crashes so far.
the app can however be run directly.
first install python, pip and virtualenv
```
sudo zypper python-devel python-pip python-virtualenv
```
then create a virtual machine and
```
pip -r requirements.txt
```
to install required packages. This takes a while.

You need to run gunicorn from root to be able to listen to port 80
```
sudo gunicorn run:app --worker-class gevent \
--workers 3 -b 0.0.0.0:80 --user=mengel --group=users
```
#### production on se51

This should be done with nginx and supervisor. It is still not working. supervisor
Supervisor serves its own web frontend instead of the website.
TODO: properly install nginx and create config templates for gunicorn, nginx
and supervisor. 


### Run with docker

For production and easy transfer between machines, the app is packaged in a docker container. You can build the container from source by
```
docker build --tag wacalc .
```

The `data` folder, which holds the cmip3 and cmip5 netCDF4 files needs to be mounted with absolute path in docker. So this is machine dependent.

To mount the data folder under `/wacalc/data` inside the container, and forward the exposed port 5000 on the container to port 5000 on the host machine, do:
```
docker run -p 5000:5000 -v \
/home/mengel/projects/wacalc/data/:/wacalc/data:ro wacalc
```
 Note the user-specific path to the data folder on the host machine.

You will be able to access the app in your browser under

http://localhost:5000/


#### Current build errors:
There is a problem with pip and netCDF4. Building the docker image gives the following error:
```python
  ----------------------------------------
  Failed building wheel for netCDF4
  Running setup.py clean for netCDF4
  Complete output from command /usr/bin/python -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-l1I7Md/netCDF4/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" clean --all:
  reading from setup.cfg...
  using nc-config ...
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
    File "/tmp/pip-build-l1I7Md/netCDF4/setup.py", line 383, in <module>
      import numpy
  ImportError: No module named numpy
```

The build continues and the app still works, however.
