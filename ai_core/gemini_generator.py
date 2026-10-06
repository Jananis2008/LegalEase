import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


# =========================
# GEMINI CLIENT
# =========================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        timeout=15000
    )
)


# =========================
# DOCUMENT GENERATOR
# =========================

class GeminiDocumentGenerator:

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        prompt = f"""
You are a professional legal document drafting assistant.

Create a clear and professional {document_type}.

Parties:
{parties}

Dates:
{dates}

Terms:
{terms}

Requirements:

1. Create a proper title.
2. Include the provided parties.
3. Include the provided dates.
4. Include all provided terms.
5. Use suitable sections and clauses for the selected document type.
6. Use professional and clear legal language.
7. Add signature sections.
8. Do not add unnecessary explanations outside the document.
9. Do not invent important facts that were not provided.
10. The output must be a complete document.

Document:
"""

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            if response.text:
                return response.text

            return self.fallback_document(
                document_type,
                parties,
                terms,
                dates
            )

        except Exception:

            return self.fallback_document(
                document_type,
                parties,
                terms,
                dates
            )


    # =========================
    # FALLBACK DOCUMENT
    # =========================

    def fallback_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        document = f"""
{document_type.upper()}

PARTIES
{parties}

DATE / TERM
{dates}

TERMS AND CONDITIONS
{terms}

GENERAL TERMS

1. The parties agree to the terms and conditions specified in this document.

2. Both parties shall comply with their respective responsibilities
and obligations stated in this document.

3. Any modification to this document should be agreed upon by the
parties in writing.

4. The information in this document is based on the details provided
by the user.

5. The document should be reviewed carefully before official use.

SIGNATURES

Party 1: ______________________________

Party 2: ______________________________

Date: __________________________________
"""

        return document