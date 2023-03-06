FROM node:16.15.0 AS builder
ADD ./frontend/package.json /frontend/package.json
WORKDIR /frontend
RUN yarn install
ADD ./frontend /frontend
RUN yarn build --base="/routes/object-detection/web/"


FROM lokoai/python_yolov7:0.0.1
EXPOSE 8080
ADD ./requirements.lock /
RUN pip install -r /requirements.lock
ARG GATEWAY
ENV GATEWAY=$GATEWAY
ADD . /plugin
COPY --from=builder /frontend/dist /frontend/dist
ENV PYTHONPATH=$PYTHONPATH:/plugin
WORKDIR /plugin/services
ENV PYTHONBUFFERED=1
CMD python -u services.py
