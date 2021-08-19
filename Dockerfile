FROM python:3.9-slim

# replicate host user to avoid file permission issues
ARG USER_ID
ARG GROUP_ID
RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user
# add scripts to path, not sure why not done automatically
ENV PATH=/home/user/.local/bin:$PATH

WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY ./ /code