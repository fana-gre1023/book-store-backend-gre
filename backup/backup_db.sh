#!/bin/bash

# Database URL
DATABASE_URL="postgres://avnadmin:AVNS_g5qSrWuMkbA3xFMD1I6@pg-2b6c4e61-gregorybeal4-8f33.l.aivencloud.com:15763/defaultdb"

# Extracting connection details from the DATABASE_URL
# HOST=$(echo $DATABASE_URL | sed -e 's/^.*@//' -e 's/:.*$//')
# PORT=$(echo $DATABASE_URL | sed -e 's/^.*://' -e 's/\/.*$//')
# USER=$(echo $DATABASE_URL | sed -e 's/^.*\/\///' -e 's/:.*$//')
# PASSWORD=$(echo $DATABASE_URL | sed -e 's/^.*://' -e 's/@.*$//')
# DB_NAME=$(echo $DATABASE_URL | sed -e 's/.*\/\([^?]*\).*/\1/')

HOST="pg-2b6c4e61-gregorybeal4-8f33.l.aivencloud.com"
PORT="15763"
USER="avnadmin"
PASSWORD="AVNS_g5qSrWuMkbA3xFMD1I6"
DB_NAME="defaultdb"


# Set the environment variable for the PostgreSQL password
export PGPASSWORD=$PASSWORD

# Set SSL mode to require
export PGSSLMODE=require

# Backup file name
BACKUP_FILE="db_backup_$(date +%Y%m%d_%H%M%S).sql"

# Run pg_dump to backup the database
pg_dump -h $HOST -p $PORT -U $USER -d $DB_NAME -F c -b -v -f $BACKUP_FILE

# Unset the PostgreSQL password and SSL mode environment variables
unset PGPASSWORD
unset PGSSLMODE

echo "Backup completed: $BACKUP_FILE"
