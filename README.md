![alt text](https://raw.githubusercontent.com/muhiza/extrat/master/static/copa_new_home_page.png)

## Smart Cooperative Platform Technical Documentation - AICOS

## Overview
This a cooperative management solution named “Automated and Integrated Cooperative System”, (AICOS). Through the system, cooperatives can greatly increase efficiency, transparency, traceability and trust.

With the platform, digitizing operations of cooperatives can help better planning, evaluation and monitoring by different stakeholders. It will help boost Rwanda’s economy by ensuring a more efficient cooperative ecosystem which counts 5 million Rwandans (55.3% of the adult population) as its members, across all areas of the economy.

Cooperatives can use the system in membership management - where they are able to record all details regarding their members - ; stock and asset management; making it possible to monitor, share, report and analyse all cooperative activities in real time, such as financial and accounting activities, administrative activities, and production activities. This can be done in different sectors of the economy such as services, agriculture, transport, trade, etc.

The AICOS, Smart Cooperative system can be used by all cooperatives sector organs such as Unions, Federations, cooperatives’ stakeholders as well as RCA, other government institutions and development partners to access different data for planning and budgeting purposes.

## Modular Approach in Smart Cooperative Platform Development

Modular programming is the process of subdividing a computer program into separate sub-programs. A module is a separate software component. It can often be used in a variety of applications and functions with other components of the system.

* Some programs might have thousands or millions of lines and to manage such programs it becomes quite difficult as there might be too many syntax errors or logical errors present in the program, so to manage such type of programs concept of modular programming approached.

* Each sub-module contains something necessary to execute only one aspect of the desired functionality.
Modular programming emphasis on breaking of large programs into small problems to increase the maintainability, readability of the code and to make the program handy to make any changes in the future or to correct the errors.

## Points which should be taken care of prior to modular program development:

* Limitations of each and every module should be decided.
* In which way a program is to be partitioned into different modules.
* Communication among different modules of the code for proper execution of the entire program.

The complete code for smart cooperative platform, Build all functionalities with as a Web Platform With Python and Flask, which you can find on copa.rw [here](https://www.copa.rw/).


### API documentation links

[Graphql API Documentation]()
[Django API Documentation]()

### Installing

```
    $ git clone https://github.com/EXTRA-TECH/copa.git
    $ cd copa
    $ python3 -m venv <your folder path>
    $ source venv/bin/activate
    $ git checkout develop

```

- Create .env and copy paste the environment variable from `.env_example` file that's already existent in the root directory

- Run the following commands

```
    $ pip install -r requirements.txt

```

- Create a postgreSQL database called copa using the default postgres user and change the value of variable DB_PASSWORD in your .env file to your postgres user's password.

- Run the following commands to make the database migrations.

```
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
```

### Running the application

Run the command below to run the application locally.

```
  $ python3 manage.py runserver

```

### Running the tests

Run the command below to run the tests for the application.

```
    $ python manage.py test

```

### Installing using docker

check Docker installation that applies to you operating system. [Docker](https://docs.docker.com/get-docker/)

if you have docker installed run the following command in the root directory/folder.

```
    $ docker build .
    $ docker-compose build
```

### Running the tests with Docker

```
    $ docker-compose run app --rm sh -c "python manage.py test"
```
### Running the application using Docker

```
    $ docker-compose up
```

### Deployment

Link: [click here](https://www.copa.rw/)

### Built With

The project has been built with the following technologies so far:

[Django](https://www.djangoproject.com/) - web framework for building websites using Python
[GraphQL](https://graphql.org/) - query language for our APIs.
[pip](https://pip.pypa.io/en/stable/) - package installer for Python
[PostgreSQL](https://www.postgresql.org/) - database management system used to persists the application's data.

