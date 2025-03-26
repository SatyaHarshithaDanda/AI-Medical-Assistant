import streamlit as st
from pathlib import Path
import google.generativeai as genai
from PIL import Image
from api_key import api_key

#Configure the API key
genai.configure(api_key=api_key)

# Set up the model configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Apply safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT", 
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH", 
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", 
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT", 
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

# Set up the system prompt
system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the image.

**Your Responsibilities:**

1. **Detailed Analysis:** Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. **Findings Report:** Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured form.
3. **Recommendations and Next Steps:** Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. **Treatment Suggestions:** If appropriate, recommend possible treatment options or interventions.

**Important Notes:**

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."
4. Your Insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide me with an output response containing these 4 headings:
* Detailed Analysis
* Findings Report
* Recommendations and Next Steps
* Treatment Suggestions

**Summary:**
- Possible Diseases: [List possible diseases or problems]
- Urgency Level: [Low / Medium / High]
- Next Steps: [Brief suggestion]

Disclaimer:
"""

# Initialize the model
model = genai.GenerativeModel( model_name="gemini-2.0-pro-exp-02-05",
                               generation_config=generation_config,
                               safety_settings=safety_settings)

# Set Streamlit page configuration
st.set_page_config(page_title="Medical Image Analytics", page_icon=":robot:")

# Set logo
logo_path = "logo.png"
logo_img = Image.open(logo_path)

# Resize the logo to the desired size
#logo_img = logo_img.resize((715, 200))

# Display the logo
st.image(logo_img, width=715)  # Set the width to 1815

# App title and subtitle
st.title("Medical Image Analytics")
st.subheader("An application that helps analyze medical images")

# File uploader for the medical image
uploaded_file = st.file_uploader("Upload a medical image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, width=300, caption="Uploaded Image")
    submit_button = st.button("Generate the Analysis")

    if submit_button:
        # Process the uploaded image
        image_data = uploaded_file.getvalue()
        
        # Prepare image data for the API request
        image_parts = [
            {
                "mime_type": "image/jpeg", 
                "data": image_data
            }
        ]

        # Prepare the prompt for the API request
        prompt_parts = [
            image_parts[0], 
            system_prompt
        ]

        # Generate a response based on prompt and image
        response = model.generate_content(prompt_parts)    
        st.title("Here is the analysis based on your image:")
        st.write(response.text)
else:
    st.write("Please upload a medical image.")
