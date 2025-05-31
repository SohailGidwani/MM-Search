#!/bin/bash

# Base URL of the running Flask server
BASE_URL="${BASE_URL:-http://localhost:5000}"

# Health check
curl "$BASE_URL/api/status"

echo -e "\n"

# System statistics
curl "$BASE_URL/api/status/stats"

echo -e "\n"

# Upload a single file
curl -X POST -F "file=@/path/to/file.pdf" "$BASE_URL/api/upload/file"

echo -e "\n"

# Upload multiple files in one request
curl -X POST \
  -F "files=@/path/to/file1.pdf" \
  -F "files=@/path/to/file2.docx" \
  "$BASE_URL/api/upload/batch"

echo -e "\n"

# Check upload processing status (replace 1 with actual ID)
curl "$BASE_URL/api/upload/status/1"

echo -e "\n"

# List all uploaded files
curl "$BASE_URL/api/files"

echo -e "\n"

# Get information about a specific file
curl "$BASE_URL/api/files/1"

echo -e "\n"

# Get processed content for a file
curl "$BASE_URL/api/files/1/content"

echo -e "\n"

# Delete a file
curl -X DELETE "$BASE_URL/api/files/1"

echo -e "\n"

# Perform a search query
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "search term"}' "$BASE_URL/api/search"

echo -e "\n"

# Get search suggestions
curl "$BASE_URL/api/search/suggestions"

echo -e "\n"

# Get search history
curl "$BASE_URL/api/search/history"

echo -e "\n"
