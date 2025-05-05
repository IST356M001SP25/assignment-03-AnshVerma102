'''
Next, write a streamlit to read ONE file of packaging information. 
You should output the parsed package and total package size for each package in the file.

Screenshot available as process_file.png
'''
import streamlit as st
import packaging
import json

st.title("Process File of Packages")

file = st.file_uploader("Upload package file:")

@st.cache_data
def parse_file(text: str):
    packages = []
    infos = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        pkg = packaging.parse_packaging(line)
        total = packaging.calc_total_units(pkg)
        unit = packaging.get_unit(pkg)
        packages.append(pkg)
        infos.append((line, total, unit))
    return packages, infos

if file:
    filename = file.name
    json_filename = filename.replace(".txt", ".json")

    # Read & decode once
    text = file.getvalue().decode("utf-8")

    # Heavy lifting only runs when `text` changes
    packages, infos = parse_file(text)

    # Display each line’s total
    for line, total, unit in infos:
        st.info(f"{line} ➡️ Total 📦 Size: {total} {unit}")

    # Dump JSON once
    count = len(packages)
    with open(f"./data/{json_filename}", "w") as f:
        json.dump(packages, f, indent=4)

    st.success(f"{count} packages written to {json_filename}", icon="💾")
