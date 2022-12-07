#!/bin/bash

# the scrip to load data into the database
# should be arranged according to dependency of models

python3 manage.py loaddata copa/fixtures/example.json
