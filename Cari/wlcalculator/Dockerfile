FROM ubuntu

MAINTAINER mengel@pik-potsdam.de

RUN apt-get update && apt-get install -y \
gunicorn \
nginx \
libnetcdf-dev \
python-dev \
python-pip

# Setup flask application
RUN mkdir -p /wacalc/app
COPY requirements.txt /wacalc/
RUN pip install -r /wacalc/requirements.txt

# copy source code. Do this after pip to make us of cache.
COPY app /wacalc/app
COPY run.py /wacalc/
COPY config.py /wacalc/

# Set the default directory where CMD will execute
WORKDIR /wacalc

# expose a port for the flask development server
EXPOSE 5000

## for debugging
#CMD ["python","run.py"]
## in production
CMD ["gunicorn", "--workers=4", "-b 0.0.0.0:5000","run:app"]