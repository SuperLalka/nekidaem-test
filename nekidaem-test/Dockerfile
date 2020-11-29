###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.3-alpine as builder

# set work directory
WORKDIR /usr/src/nekidaem-test

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# lint
RUN pip install --upgrade pip
COPY . .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/nekidaem-test/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.8.3-alpine

# create directory for the app user
RUN mkdir -p /home/nekidaem-test

# create the app user
RUN addgroup -S nekidaem-test && adduser -S nekidaem-test -G nekidaem-test

# create the appropriate directories

ENV HOME=/home/nekidaem-test
ENV APP_HOME=/home/nekidaem-test/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/nekidaem-test/wheels /wheels
COPY --from=builder /usr/src/nekidaem-test/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R nekidaem-test:nekidaem-test $APP_HOME

# change to the app user
USER nekidaem-test

# run entrypoint.prod.sh
ENTRYPOINT ["/home/nekidaem-test/web/entrypoint.sh"]