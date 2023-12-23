FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN yum install -y krb5-devel
RUN yum install -y gcc
RUN pip install gssapi
RUN pip install -r requirements.txt

COPY src/main.py ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]