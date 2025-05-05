'''
In this final program, you will re-write your `process_file.py` 
to keep track of the number of files and total number of lines 
that have been processed.

For each file you read, you only need to output the 
summary information eg. "X packages written to file.json".

Screenshot available as process_files.png
'''
import streamlit as st
import packaging
from io import StringIO
import json

st.title("Process Package Files")

# initialize
if 'summaries' not in st.session_state:
    st.session_state.summaries = []
if 'total_lines' not in st.session_state:
    st.session_state.total_lines = 0
if 'total_files' not in st.session_state:
    st.session_state.total_files = 0

# ui
file = st.file_uploader("Upload package file:")

@st.cache_data
def parse_packages(text: str):
    packages = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        packages.append(packaging.parse_packaging(line))
    return packages

# when there is a file....
if file:
    filename = file.name
    json_filename = filename.replace(".txt", ".json")

    # decode once
    text = file.getvalue().decode("utf-8")
    # parse only when text changes
    packages = parse_packages(text)

    count = len(packages)
    with open(f"./data/{json_filename}", "w") as f:
        json.dump(packages, f, indent=4)

    summary = f"{count} packages written to {json_filename}"
    # update session state
    st.session_state.summaries.append(summary)
    st.session_state.total_files += 1
    st.session_state.total_lines += count

    # summarize
    for s in st.session_state.summaries:
        st.info(s, icon="💾")

    st.success(
        f"{st.session_state.total_files} files processed, "
        f"{st.session_state.total_lines} total lines processed"
    )
