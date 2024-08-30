#!/bin/bash
# Combined Backup Script

DATE=$(date +%F)
BACKUP_DIR="/home/username/backup/$DATE"
STATIC_DIR="/home/username/your_django_project/staticfiles"
MEDIA_DIR="/home/username/your_django_project/media"

# Create backup directory if it does not exist
mkdir -p $BACKUP_DIR

# Backup code (Git)
cd /home/username/your_django_project
if [[ $(git status -s) ]]; then
    git add .
    git commit -m "Automated backup on $(date)"
    git push origin main
fi

# Backup static and media files
tar -czvf $BACKUP_DIR/static_backup.tar.gz $STATIC_DIR
tar -czvf $BACKUP_DIR/media_backup.tar.gz $MEDIA_DIR
