import os
import streamlit as st
import requests

from utils.formatter import (
    save_as_txt,
    save_as_docx,
    save_as_pdf,
    format_html_preview
)


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# =========================
# CUSTOM UI STYLE
# =========================

st.markdown(
    """
    <style>

        [data-testid="stMainBlockContainer"] {
            padding-bottom: 80px !important;
        }


        /* =========================
           GENERATE BUTTON
        ========================= */

        div.stButton > button[kind="primary"] {
            width: 100% !important;
            min-height: 52px !important;

            background: #D4AF37 !important;
            color: white !important;

            border: 2px solid #D4AF37 !important;
            border-radius: 10px !important;

            font-size: 17px !important;
            font-weight: 700 !important;

            box-shadow: none !important;
            transform: none !important;
        }

        div.stButton > button[kind="primary"]:hover {
            background: #B8860B !important;
            color: white !important;

            border: 2px solid #B8860B !important;

            box-shadow: none !important;
            transform: none !important;
        }


        /* =========================
           NORMAL BUTTONS
        ========================= */

        div.stButton > button:not([kind="primary"]) {
            width: 100% !important;
            min-height: 50px !important;

            background: white !important;
            color: #6B5310 !important;

            border: 2px solid #D4AF37 !important;
            border-radius: 10px !important;

            font-size: 16px !important;
            font-weight: 700 !important;

            box-shadow: none !important;
            transform: none !important;
        }

        div.stButton > button:not([kind="primary"]):hover {
            background: #FFF8E1 !important;
            color: #6B5310 !important;

            border: 2px solid #D4AF37 !important;

            box-shadow: none !important;
            transform: none !important;
        }


        /* =========================
           DOWNLOAD BUTTONS
        ========================= */

        div.stDownloadButton > button {
            width: 100% !important;
            min-height: 52px !important;

            background: white !important;
            color: #6B5310 !important;

            border: 2px solid #D4AF37 !important;
            border-radius: 10px !important;

            font-size: 15px !important;
            font-weight: 700 !important;

            box-shadow: none !important;
            transform: none !important;

            transition: none !important;
        }

        div.stDownloadButton > button:hover {
            background: #FFF8E1 !important;
            color: #6B5310 !important;

            border: 2px solid #D4AF37 !important;

            box-shadow: none !important;
            transform: none !important;
        }


        /* =========================
           DOWNLOAD TITLE
        ========================= */

        .download-title {
            text-align: center;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 18px;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# LEGAL EASE BRANDING
# =========================

st.image(
    "assets/LegalEase_logo.png",
    width=250
)

st.subheader(
    "AI-Powered Legal Document Generator"
)


# =========================
# DOCUMENT INPUTS
# =========================

document_type = st.selectbox(
    "Document Type",
    [
        "Employment Contract",
        "Lease Agreement",
        "Non-Disclosure Agreement (NDA)"
    ]
)


parties = st.text_area(
    "Parties",
    placeholder="Example: Company ABC and John Doe",
    height=100
)


terms = st.text_area(
    "Terms",
    placeholder=(
        "Example: Salary: ₹30,000; Duration: 1 year; "
        "Notice period: 30 days"
    ),
    height=120
)


dates = st.text_input(
    "Dates",
    placeholder=(
        "Example: January 1, 2027 to December 31, 2027"
    )
)


# =========================
# SESSION STATE
# =========================

if "generated_document" not in st.session_state:
    st.session_state.generated_document = None

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "txt_data" not in st.session_state:
    st.session_state.txt_data = None

if "docx_data" not in st.session_state:
    st.session_state.docx_data = None

if "pdf_data" not in st.session_state:
    st.session_state.pdf_data = None


# =========================
# CREATE DOWNLOAD FILES
# =========================

def create_download_files(content):

    os.makedirs("temp", exist_ok=True)

    # -------------------------
    # TXT
    # -------------------------

    txt_path = "temp/LegalEase_Document.txt"

    save_as_txt(
        content,
        txt_path
    )

    with open(txt_path, "rb") as file:
        st.session_state.txt_data = file.read()


    # -------------------------
    # DOCX
    # -------------------------

    docx_path = "temp/LegalEase_Document.docx"

    save_as_docx(
        content,
        docx_path
    )

    with open(docx_path, "rb") as file:
        st.session_state.docx_data = file.read()


    # -------------------------
    # PDF
    # -------------------------

    pdf_path = "temp/LegalEase_Document.pdf"

    save_as_pdf(
        content,
        pdf_path
    )

    with open(pdf_path, "rb") as file:
        st.session_state.pdf_data = file.read()


# =========================
# GENERATE DOCUMENT
# =========================

if st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True
):

    if not parties or not terms or not dates:

        st.warning(
            "Please fill in all the fields."
        )

    else:

        try:

            response = requests.post(
                "http://127.0.0.1:8000/generate",
                json={
                    "document_type": document_type,
                    "parties": parties,
                    "terms": terms,
                    "dates": dates
                },
                timeout=120
            )

            if response.status_code == 200:

                result = response.json()

                document = result["document"]

                st.session_state.generated_document = document

                st.session_state.edit_mode = False

                # Create files ONLY when document is generated
                create_download_files(document)

                st.success(
                    "Document generated successfully!"
                )

            else:

                st.error(
                    "Something went wrong. "
                    "Please check the FastAPI server."
                )

        except requests.exceptions.RequestException:

            st.error(
                "Unable to connect to the LegalEase backend. "
                "Please make sure FastAPI is running."
            )


# =========================
# DISPLAY GENERATED DOCUMENT
# =========================

if st.session_state.generated_document:

    st.divider()

    st.subheader(
        "📄 Document Preview"
    )


    # =========================
    # HTML PREVIEW
    # =========================

    preview_html = format_html_preview(
        st.session_state.generated_document
    )

    st.markdown(
        preview_html,
        unsafe_allow_html=True
    )


    # =========================
    # EDIT DOCUMENT
    # =========================

    st.divider()

    if not st.session_state.edit_mode:

        if st.button(
            "✏️ Edit Document",
            use_container_width=True
        ):

            st.session_state.edit_mode = True

            st.rerun()


    else:

        st.info(
            "You can edit the document below."
        )

        edited_document = st.text_area(
            "Edit Document",
            st.session_state.generated_document,
            height=500
        )

        col1, col2 = st.columns(
            2,
            gap="medium"
        )


        # =========================
        # SAVE CHANGES
        # =========================

        with col1:

            if st.button(
                "💾 Save Changes",
                use_container_width=True
            ):

                st.session_state.generated_document = (
                    edited_document
                )

                st.session_state.edit_mode = False

                # Recreate files ONLY after editing
                create_download_files(
                    edited_document
                )

                st.success(
                    "Changes saved successfully!"
                )

                st.rerun()


        # =========================
        # CANCEL
        # =========================

        with col2:

            if st.button(
                "❌ Cancel",
                use_container_width=True
            ):

                st.session_state.edit_mode = False

                st.rerun()


    # =========================
    # DOWNLOAD SECTION
    # =========================

    st.divider()

    st.markdown(
        """
        <div class="download-title">
            📥 Download Document
        </div>
        """,
        unsafe_allow_html=True
    )


    # =========================
    # DOWNLOAD BUTTONS
    # =========================

    download_col1, download_col2, download_col3 = st.columns(
        [1, 1, 1],
        gap="large"
    )


    # =========================
    # TXT
    # =========================

    with download_col1:

        st.download_button(
            label="📄 Download TXT",
            data=st.session_state.txt_data,
            file_name="LegalEase_Document.txt",
            mime="text/plain",
            use_container_width=True,
            on_click="ignore"
        )


    # =========================
    # DOCX
    # =========================

    with download_col2:

        st.download_button(
            label="📝 Download DOCX",
            data=st.session_state.docx_data,
            file_name="LegalEase_Document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
            on_click="ignore"
        )


    # =========================
    # PDF
    # =========================

    with download_col3:

        st.download_button(
            label="📕 Download PDF",
            data=st.session_state.pdf_data,
            file_name="LegalEase_Document.pdf",
            mime="application/pdf",
            use_container_width=True,
            on_click="ignore"
        )