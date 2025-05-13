import streamlit as st
import requests
from htbuilder import HtmlElement, div, p, a, styles
from htbuilder.units import percent, px

st.set_page_config(page_title="API Key Tester", page_icon="🔑", layout="centered")
st.title("🔑 API Key Tester")

st.markdown(
    '<div style="background-color:#ffdddd;border-left:6px solid #f44336;padding:12px 16px;margin-bottom:18px;font-weight:bold;color:#a94442;">'
    'User API keys are not stored. They are only used for this session and never saved.'
    '</div>',
    unsafe_allow_html=True
)

PROVIDERS = {
    "OpenAI": {
        "endpoint": "https://api.openai.com/v1/models",
        "header": lambda key: {"Authorization": f"Bearer {key}"},
        "test_info": "Lists available models."
    },
    "Google AI": {
        "endpoint": "https://generativelanguage.googleapis.com/v1/models",
        "header": lambda key: {"Authorization": f"Bearer {key}"},
        "test_info": "Lists available models. Requires API key as Bearer token."
    },
    "Anthropic": {
        "endpoint": "https://api.anthropic.com/v1/models",
        "header": lambda key: {"x-api-key": key},
        "test_info": "Lists available models."
    },
    "Huggingface": {
        "endpoint": "https://huggingface.co/api/models",
        "header": lambda key: {"Authorization": f"Bearer {key}"},
        "test_info": "Lists available models."
    },
    "OpenAI Compatible": {
        "endpoint": "",
        "header": lambda key: {"Authorization": f"Bearer {key}"},
        "test_info": "Enter your custom endpoint."
    }
}

provider = st.selectbox("Select Provider", list(PROVIDERS.keys()))

api_key = st.text_input("API Key", type="password")

endpoint = PROVIDERS[provider]["endpoint"]
if provider == "OpenAI Compatible":
    endpoint = st.text_input("Custom Endpoint URL", value=endpoint)

headers = PROVIDERS[provider]["header"](api_key) if api_key else {}

st.info(PROVIDERS[provider]["test_info"])

params = st.text_area("Optional Query Parameters (JSON)", "{}")

if st.button("Test API Key"):
    if not api_key:
        st.error("Please enter an API key.")
    elif not endpoint:
        st.error("Please enter a valid endpoint URL.")
    else:
        try:
            query_params = {}
            if params.strip():
                import json
                query_params = json.loads(params)
            resp = requests.get(endpoint, headers=headers, params=query_params, timeout=10)
            st.write(f"**Status Code:** {resp.status_code}")
            try:
                st.json(resp.json())
            except Exception:
                st.text(resp.text)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.markdown("*Supports OpenAI, Google AI, Anthropic, Huggingface, and custom OpenAI-compatible endpoints.*")

# --- Custom Footer ---

def layout(*args):
    style = """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      .stApp { bottom: 70px; }
    </style>
    """
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="gray",
        text_align="center",
        font_size="0.9em",
        height="auto",
        opacity=1,
        background_color="rgba(14, 17, 23, 0.95)"
    )
    body = p()
    foot = div(style=style_div)(body)
    st.markdown(style, unsafe_allow_html=True)
    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)
    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    layout(
        "Made with ❤️ by ",
        a(_href="https://github.com/HomeDev68", _target="_blank")("HomeDev68")
    )

footer()
