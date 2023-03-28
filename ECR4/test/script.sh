#!/bin/bash

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 725312303732.dkr.ecr.us-east-2.amazonaws.com
docker build -f /home/sxnity/Desktop/trainee/ECR4/test/Dockerfile /home/sxnity/Desktop/trainee/ECR4/test/
a=( $(docker images | awk '{print $3}') )
echo ${a[1]}
docker tag ${a[1]} 725312303732.dkr.ecr.us-east-2.amazonaws.com/test1-private:v4
docker push 725312303732.dkr.ecr.us-east-2.amazonaws.com/test1-private:v4