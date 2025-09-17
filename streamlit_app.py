import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

# Add some spacing
''
''
import streamlit as st
from PIL import Image
import pytesseract
import re

st.title("מחשבון ממוצע מועד ב׳ מתמונה")

uploaded_a = st.file_uploader("העלה תמונה של התפלגות מועד א׳", type=["png","jpg","jpeg"])
uploaded_b = st.file_uploader("העלה תמונה של התפלגות מועד ב׳", type=["png","jpg","jpeg"])

def extract_distribution(img):
    text = pytesseract.image_to_string(img, lang="eng")  # OCR
    # מחפשים אחוזים בטקסט (למשל "58.9%")
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*%", text)
    values = [float(m) for m in matches]
    return values, text

def compute_avg_B_only(distA, distB, ranges):
    deltas = []
    for (r,a), (_,b) in zip(distA, distB):
        delta = b - a
        deltas.append((r, delta))

    positive = [(r,d) for (r,d) in deltas if d > 0]
    if not positive:
        return None
    
    num = sum(((r[0]+r[1])/2)*d for r,d in positive)
    den = sum(d for _,d in positive)
    return num/den if den else None

ranges = [
    (0,59),
    (60,64),
    (65,74),
    (75,84),
    (85,89),
    (90,94),
    (95,100)
]

if uploaded_a and uploaded_b:
    img_a = Image.open(uploaded_a)
    img_b = Image.open(uploaded_b)

    distA, textA = extract_distribution(img_a)
    distB, textB = extract_distribution(img_b)

    st.subheader("OCR מועד א׳")
    st.text(textA)
    st.subheader("OCR מועד ב׳")
    st.text(textB)

    if len(distA) == len(ranges) and len(distB) == len(ranges):
        avg = compute_avg_B_only(list(zip(ranges, distA)), list(zip(ranges, distB)), ranges)
        if avg:
            st.success(f"ממוצע מועד ב׳ בלבד: {avg:.2f}")
        else:
            st.error("לא נמצאו שיפורים במועד ב׳.")
    else:
        st.warning("לא זוהו מספיק טווחים מהתמונה – בדוק שהתמונה ברורה.")

            value=f'{last_gdp:,.0f}B',
            delta=growth,
            delta_color=delta_color
        )
