#! /usr/bin/env bash

# Let the DB start
python /rook/rook_prestart.py

# Run migrations
alembic upgrade head
