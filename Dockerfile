FROM ghcr.io/imagination-ai/base-python:main as base

RUN mkdir -p /build/tests
RUN mkdir /applications

COPY requirements.txt /build/requirements.txt
RUN pip3 install -r /build/requirements.txt

#RUN pip3 install \ #  --no-color --progress-bar off \
    #-r /build/requirements.txt \
    #-r /build/requirements-test.txt # | ts -i '%.S'

COPY requirements-test.txt /build/requirements-test.txt
RUN pip3 install -r /build/requirements-test.txt

COPY .isort.cfg /build/.isort.cfg
COPY pytest.ini /build/pytest.ini
COPY .flake8 /build/.flake8


ENV APP_RESOURCE_DIR /applications
ENV PYTHONPATH /applications

ARG skip_tests

##### 1. Leaf Image: Signs #####
FROM base as nonvital-vital-signs

COPY src/signs /build/signs
COPY tests/signs/tests /build/tests


RUN \
    if [ "$skip_tests" = "" ] ; then \
        black \
           -t py39 -l 80 \
           --check $(find /build/signs /build/tests -name "*.py") \
      && \
        # isort --df --settings-path=/build/.isort.cfg --check /build/signs \
      #&& \
        flake8 --config=/build/.flake8 /build/signs \
      && \
        pytest /build/tests ; \
      else \
        echo "Skipping tests" ; \
    fi

RUN mv /build/signs /applications/signs
EXPOSE 8080

COPY entrypoints/signs-app-entrypoint.sh /applications/signs-app-entrypoint.sh
ENTRYPOINT ["sh", "/applications/signs-app-entrypoint.sh"]
