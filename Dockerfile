FROM python:3

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir pandas \
  && pip install --no-cache-dir canvas_selector \ 
  && pip install --no-cache-dir PeerMark


COPY .canvasapirc ./root/
