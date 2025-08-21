# Your Text, Your Style — PPT Generator (Starter)

This repository contains a starter Streamlit app and helper modules to convert bulk text or markdown into a PowerPoint presentation using an LLM to plan slides and `python-pptx` to construct the file.

## Features (MVP)
- Paste large text input (markdown or prose)
- Optional one-line guidance
- Upload a .pptx/.potx template to reuse styles
- Provide your LLM API key (used in-memory only)
- Download generated .pptx

## Quickstart (local)
1. Create and activate a Python environment (Python 3.9+).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Notes
- The app attempts to use the `openai` package if available; you can adapt `utils/llm_utils.py` to support other providers.
- Do **not** store API keys. The app uses the key only for the request.
- Example template provided in `examples/` — replace with your own template for best results.

## License
MIT
