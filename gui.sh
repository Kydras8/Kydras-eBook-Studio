#!/bin/bash

zenity --file-selection --multiple --title="Select files to convert to eBook" --file-filter="*.pdf *.txt *.md *.py" > /tmp/input_files.txt

if [ ! -s /tmp/input_files.txt ]; then
    zenity --error --text="No files selected. Exiting."
    exit 1
fi

for file in $(cat /tmp/input_files.txt | tr '|' '\n'); do
    python3 webui/terminal-server.py "$file"
done

zenity --info --text="Conversion complete!"
