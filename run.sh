#!/bin/bash
app=`basename $(pwd)`
docker image build -t ${app} .
docker container run \
  -p 5000:5000 \
  --rm \
  --name=${app} \
  -v $PWD:/app \
  ${app}
