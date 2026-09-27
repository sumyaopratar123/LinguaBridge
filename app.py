import requests
import streamlit as st
from urllib.parse import quote

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu"
}

API_URL = "https://api.mymemory.translated.net/get"

st.set_page_config(
    page_title="LinguaBridge",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 LinguaBridge")
st.caption("Multilingual Language Translation Tool")

col1, col2 = st.columns(2)

with col1:
    source_name = st.selectbox(
        "Source language",
        list(LANGUAGES.keys()),
        index=0
    )

with col2:
    target_name = st.selectbox(
        "Target language",
        list(LANGUAGES.keys()),
        index=2
    )

text = st.text_area(
    "Enter text",
    height=180,
    placeholder="Type your text here..."
)


def translate_text(text, source, target):

    params = {
        "q": text,
        "langpair": f"{source}|{target}"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    if result.get("responseStatus") != 200:
        raise Exception(
            result.get(
                "responseDetails",
                "Translation service error"
            )
        )

    translated = result["responseData"]["translatedText"]

    if not translated:
        raise Exception("No translation returned.")

    return translated


if st.button(
    "Translate",
    type="primary",
    use_container_width=True
):

    if not text.strip():

        st.warning("Please enter some text.")

    elif source_name == target_name:

        translated = text.strip()

        st.info(
            "Source and target languages are the same."
        )

        st.subheader("Translation")
        st.success(translated)

        st.download_button(
            "⬇️ Download translation",
            translated,
            file_name="translation.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:

        source = LANGUAGES[source_name]
        target = LANGUAGES[target_name]

        try:

            with st.spinner("Translating..."):

                translated = translate_text(
                    text.strip(),
                    source,
                    target
                )

            st.subheader("Translation")
            st.success(translated)

            st.download_button(
                "⬇️ Download translation",
                translated,
                file_name="translation.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.caption(
                "Translation completed successfully."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Internet connection could not be established."
            )

        except requests.exceptions.Timeout:

            st.error(
                "Translation service timed out. Please try again."
            )

        except Exception as exc:

            st.error("Translation failed.")

            with st.expander("Technical details"):
                st.code(str(exc))


st.divider()

st.caption(
    "Technology: Python • Streamlit • "
    "MyMemory Translation API"
)