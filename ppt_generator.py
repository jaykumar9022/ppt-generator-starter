import io, json
from utils.llm_utils import call_llm_for_slide_plan
from utils.pptx_utils import build_presentation_from_plan

def generate_pptx_from_text(text, guidance, api_key, template_file, model="gpt-4o-mini"):
    # Get slide plan from LLM (expects a JSON array of slide defs)
    plan = call_llm_for_slide_plan(text, guidance, api_key, model=model)
    # Build PPTX bytes using the uploaded template (a file-like object)
    template_stream = io.BytesIO(template_file.read())
    out_bytes = build_presentation_from_plan(plan, template_stream)
    return out_bytes
