#!/bin/sh
cd /app/reveal.js
# Dynamiskt stöd för presentation och teman
npx serve --port 8000 --single --content ../presentation.md --theme custom