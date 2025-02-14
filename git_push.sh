#!/bin/bash

# Add all changes
git add .

# Commit with timestamp and message
git commit -m "update: $(date +"%Y-%m-%d %H:%M:%S") - Code improvements and fixes"

# Push to main branch
git push origin main