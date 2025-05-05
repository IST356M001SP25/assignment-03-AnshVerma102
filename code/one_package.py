'''
Write a streamlit to input one string of package data. 
It should use the `packaging.py` module to parse the string 
and output the package info as it appears. 
Calculate the total package size and display that.

see one_package.png for a screenshot
'''
import streamlit as st
import packaging

st.title("Process One Package")

pkg = st.text_input("Enter package data:")

# Cache the parsed result so we only do the heavy work when pkg changes
if "prev_pkg" not in st.session_state or st.session_state.prev_pkg != pkg:
    st.session_state.prev_pkg = pkg
    st.session_state.parsed_pkg = packaging.parse_packaging(pkg) if pkg else []

parsed_pkg = st.session_state.parsed_pkg

if parsed_pkg:
    total = packaging.calc_total_units(parsed_pkg)
    unit = packaging.get_unit(parsed_pkg)

    # Display the raw parse once
    st.write(parsed_pkg)

    # Unpack each dict without creating extra lists
    for item in parsed_pkg:
        name, size = next(iter(item.items()))
        st.info(f"{name} ➡️ {size}")

    st.success(f"Total 📦 Size: {total} {unit}")
