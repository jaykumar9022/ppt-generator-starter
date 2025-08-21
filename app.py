import streamlit as st
from ppt_generator import generate_pptx_from_text
from fastapi import FastAPI

app = FastAPI()

st.set_page_config(page_title="Your Text, Your Style — PPT Generator", layout="wide")
st.title("Your Text, Your Style — PPT Generator")

st.markdown("Paste a large block of text (markdown or prose), upload a PowerPoint template, enter an optional guidance line, and provide your LLM API key (used in-memory only).")

col1, col2 = st.columns([3,1])

with col1:
    text = st.text_area("Paste your text (markdown or prose)", height=300, key="text")
    guidance = st.text_input("One-line guidance (optional) — e.g., 'Investor pitch'", key="guidance")
    template_file = st.file_uploader("Upload a PowerPoint template (.pptx/.potx)", type=['pptx','potx'])
with col2:
    st.write("⚠️ API keys are used only for this request and not stored.")
    api_key = st.text_input("LLM API key (will not be stored)", type="password", key="api_key")
    model = st.selectbox("Model (provider-specific)", ["gpt-4o-mini", "gpt-4o", "gpt-4"], index=0)

if st.button("Generate Presentation"):
    if not text:
        st.error("Please paste the input text.")
    elif not api_key:
        st.error("Please enter your LLM API key.")
    elif not template_file:
        st.error("Please upload a PowerPoint template (.pptx/.potx).")
    else:
        try:
            with st.spinner("Generating presentation..."):
                pptx_bytes = generate_pptx_from_text(text, guidance, api_key, template_file, model=model)
                st.success("Presentation generated successfully.")
                st.download_button("Download presentation", data=pptx_bytes, file_name="generated_presentation.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
        except Exception as e:
            st.error(f"Error: {e}")


@app.get("/")
def home():
    return {"message": "Hello PPT Generator!"}            
