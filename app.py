import os
import io
import base64
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    """
    Generate content using the Gemini AI model.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    """
    Convert the uploaded PDF to images and then to base64-encoded JPEG format.
    """
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Encode to base64
        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def main():
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(page_title="ATS Resume Expert", layout="wide")

    st.title("ATS Tracking System")
    st.write("Welcome to the ATS Tracking System. Upload your resume and get detailed insights based on job descriptions.")

    # Sidebar for file upload and input
    with st.sidebar:
        st.header("Upload and Analysis")
        input_text = st.text_area("Job Description: ", key="input")
        uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

        # Dropdown menu for analysis type
        analysis_option = st.selectbox(
            "Select Analysis Type",
            [
                "Resume Evaluation",
                "Skill Improvement",
                "Percentage Match",
                "Keywords Missing",
                "Resume Formatting Suggestions",
                "Cover Letter Review",
                "Interview Preparation Tips",
                "Salary Expectation Analysis",
                "Career Path Suggestions",
                "Soft Skills Evaluation",
                "LinkedIn Profile Optimization",
                "Networking Tips",
                "Technical Skill Gap Analysis",
                "Project Experience Evaluation",
                "Certifications and Courses Recommendations",
                "Industry-Specific Insights",
                "Work-Life Balance Tips",
                "Remote Work Suitability",
                "Role Transition Strategy",
                "Freelancing Skills Assessment",
                "Freelancer Portfolio Enhancement",
                "Freelancing Market Demand Analysis",
                "Role-Specific Skill Development Plan",
                "Building a Personal Brand for Freelancing",
                "Freelancing Networking Strategies",
                "Freelance Contract and Pricing Advice",
                "Freelancing Tools and Resources Recommendations",
                "Freelance Project Management Tips"
            ],
            help="Choose the type of analysis you want to perform."
        )

        st.write("For detailed analysis, click on the corresponding button below.")
        submit_button = st.button("Perform Analysis")

    if uploaded_file:
        st.sidebar.write("PDF Uploaded Successfully")

    if submit_button:
        if uploaded_file:
            pdf_parts = input_pdf_setup(uploaded_file)
            st.spinner(text="Generating response...")

            # Define prompts
            prompts = {
                "Resume Evaluation": "As a highly experienced career consultant with a deep understanding of industry standards, evaluate the provided resume against the given job description. Provide a thorough assessment of the candidate's qualifications, including strengths and weaknesses, and offer actionable recommendations to enhance their suitability for the role.",
                "Skill Improvement": "Analyze the candidate’s technical and soft skills in relation to the job description. Identify specific skill gaps and provide a detailed plan for skill enhancement, including relevant courses, certifications, and practical steps to improve proficiency.",
                "Percentage Match": "Calculate the percentage match between the candidate's resume and the job description using advanced matching criteria. Provide a detailed breakdown of the match, including an analysis of how well the resume aligns with each requirement and suggestions for closing any gaps.",
                "Keywords Missing": "Conduct a comprehensive analysis of the resume and job description to identify missing keywords or phrases. Explain the significance of these keywords and provide a list of recommended terms to enhance the resume’s alignment with the job requirements.",
                "Resume Formatting Suggestions": "Review the formatting of the resume with a focus on professional presentation. Offer detailed suggestions to improve visual appeal, readability, and effectiveness, addressing aspects such as layout, font choice, section headings, and overall design.",
                "Cover Letter Review": "Evaluate the effectiveness of the provided cover letter in complementing the resume and addressing the job description. Provide a detailed critique on its structure, content, and how well it communicates the candidate's fit for the position, with suggestions for refinement.",
                "Interview Preparation Tips": "Based on the resume and job description, provide targeted advice for preparing for an interview. Include strategies for handling common interview questions, addressing potential challenges, and presenting key qualifications in a compelling manner.",
                "Salary Expectation Analysis": "Analyze the candidate’s salary expectations in the context of the job description and industry standards. Provide insights into the reasonableness of these expectations and suggest adjustments based on current market conditions and the candidate’s experience level.",
                "Career Path Suggestions": "Based on the candidate’s resume and job description, offer well-researched recommendations for potential career paths. Include advice on exploring new roles or industries, leveraging current skills, and positioning oneself for future opportunities.",
                "Soft Skills Evaluation": "Assess the soft skills highlighted in the resume and their relevance to the job description. Provide a detailed evaluation of how these skills align with the role and suggest areas for further development to enhance the candidate’s overall profile.",
                "LinkedIn Profile Optimization": "Review the candidate’s LinkedIn profile in relation to their resume and job description. Offer a comprehensive set of recommendations for optimizing the profile to enhance visibility, engagement, and alignment with career goals.",
                "Networking Tips": "Provide expert advice on effective networking strategies tailored to the candidate’s career goals and job description. Include specific tactics for building professional relationships, leveraging social media, and participating in industry events to expand their network.",
                "Technical Skill Gap Analysis": "Conduct a detailed analysis of the technical skills listed on the resume compared to those required by the job description. Identify any gaps and offer a strategic plan for acquiring necessary skills, including recommended resources and training programs.",
                "Project Experience Evaluation": "Evaluate the project experience detailed in the resume. Provide a thorough assessment of how these projects are presented, their relevance to the job description, and suggestions for enhancing their impact and effectiveness in showcasing the candidate’s expertise.",
                "Certifications and Courses Recommendations": "Based on the job description and resume, recommend relevant certifications and courses that can enhance the candidate’s qualifications. Provide details on how these certifications will benefit the candidate and improve their prospects for the role.",
                "Industry-Specific Insights": "Offer an in-depth analysis of industry-specific trends, challenges, and opportunities based on the resume and job description. Provide actionable insights on how the candidate can align their skills and experience with these industry dynamics.",
                "Work-Life Balance Tips": "Provide expert recommendations for maintaining a healthy work-life balance based on the job description and the candidate’s career goals. Include practical strategies for managing stress, setting boundaries, and achieving a balanced lifestyle.",
                "Remote Work Suitability": "Assess the candidate’s suitability for remote work based on their resume and the job description. Offer a detailed analysis of their skills and experience in relation to remote work requirements, and suggest any adjustments to better prepare for remote roles.",
                "Role Transition Strategy": "Develop a comprehensive strategy for transitioning to a new role or industry based on the candidate’s resume and job description. Include actionable steps for acquiring new skills, building a relevant network, and adapting to the new role effectively.",
                "Freelancing Skills Assessment": "Evaluate the skills necessary for a successful freelancing career based on the resume and job description. Provide detailed recommendations for developing these skills, including practical advice for transitioning to freelance work and building a strong client base.",
                "Freelancer Portfolio Enhancement": "Review the freelancer’s portfolio and offer expert suggestions for enhancing its quality and impact. Focus on improving presentation, showcasing key projects, and aligning the portfolio with industry standards and client expectations.",
                "Freelancing Market Demand Analysis": "Analyze the current market demand for freelance work in the candidate’s field based on their resume and job description. Provide insights into trends, opportunities, and strategies for positioning oneself effectively in the freelance market.",
                "Role-Specific Skill Development Plan": "Create a detailed skill development plan for transitioning into a new role based on the candidate’s resume and job description. Include specific recommendations for training programs, certifications, and practical experience needed to excel in the new role.",
                "Building a Personal Brand for Freelancing": "Guide the candidate on developing and enhancing their personal brand for freelancing. Provide comprehensive advice on marketing strategies, building an online presence, and positioning oneself as a leader in their freelance niche.",
                "Freelancing Networking Strategies": "Offer strategic advice on networking for freelancers. Include tactics for connecting with potential clients, leveraging industry connections, and using social media effectively to build and maintain a professional network.",
                "Freelance Contract and Pricing Advice": "Provide expert guidance on drafting freelance contracts and setting pricing strategies. Include tips on creating clear agreements, negotiating terms, and determining fair rates based on industry standards and the freelancer’s expertise.",
                "Freelancing Tools and Resources Recommendations": "Recommend essential tools and resources for freelancers to manage their work effectively. Include suggestions for project management, client communication, and productivity tools that can streamline operations and enhance efficiency.",
                "Freelance Project Management Tips": "Offer professional advice on managing freelance projects successfully. Include strategies for time management, client communication, project planning, and delivering high-quality results on time and within budget."
            }

            prompt = prompts.get(analysis_option, "Invalid option selected.")
            if prompt != "Invalid option selected.":
                response = get_gemini_response(input_text, pdf_parts, prompt)
                st.subheader("Response")
                st.write(response)
            else:
                st.write("Please select a valid analysis type.")
        else:
            st.sidebar.write("Please upload the resume")

if __name__ == "__main__":
    main()

# import os
# import io
# import base64
# from dotenv import load_dotenv
# import streamlit as st
# from PIL import Image
# import pdf2image
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure Google Generative AI
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input_text, pdf_content, prompt):
#     """
#     Generate content using the Gemini AI model.
#     """
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([input_text, pdf_content[0], prompt])
#     return response.text

# def input_pdf_setup(uploaded_file):
#     """
#     Convert the uploaded PDF to images and then to base64-encoded JPEG format.
#     """
#     if uploaded_file is not None:
#         # Convert the PDF to image
#         images = pdf2image.convert_from_bytes(uploaded_file.read())
#         first_page = images[0]

#         # Convert to bytes
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         # Encode to base64
#         pdf_parts = [{
#             "mime_type": "image/jpeg",
#             "data": base64.b64encode(img_byte_arr).decode()
#         }]
#         return pdf_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# def main():
#     """
#     Main function to run the Streamlit app.
#     """
#     st.set_page_config(page_title="ATS Resume Expert")
#     st.header("ATS Tracking System")
    
#     input_text = st.text_area("Job Description:", key="input")
#     uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

#     if uploaded_file is not None:
#         st.write("PDF Uploaded Successfully")

#     # Buttons for different functionalities
#     submit1 = st.button("Tell Me About the Resume")
#     submit2 = st.button("How Can I Improve my Skills")
#     submit3 = st.button("Percentage Match")
#     submit4 = st.button("What Are the Keywords That Are Missing")
#     submit5 = st.button("Resume Formatting Suggestions")
#     submit6 = st.button("Review My Cover Letter")
#     submit7 = st.button("Interview Preparation Tips")
#     submit8 = st.button("Salary Expectation Analysis")
#     submit9 = st.button("Career Path Suggestions")
#     submit10 = st.button("Evaluate My Soft Skills")
#     submit11 = st.button("Optimize My LinkedIn Profile")
#     submit12 = st.button("Networking Tips")
#     submit13 = st.button("Technical Skill Gap Analysis")
#     submit14 = st.button("Project Experience Evaluation")
#     submit15 = st.button("Certifications and Courses Recommendations")
#     submit16 = st.button("Industry-Specific Insights")
#     submit17 = st.button("Work-Life Balance Tips")
#     submit18 = st.button("Remote Work Suitability Analysis")

#     input_prompt1 = """
#     You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
#     Please share your professional evaluation on whether the candidate's profile aligns with the role.
#     Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
#     """

#     input_prompt2 = """
#     As a seasoned career coach with expertise in technical skills development, review the provided resume and job description.
#     Identify specific areas where the candidate can improve their skills to better align with the job requirements.
#     Provide actionable recommendations and resources that the candidate can use to enhance their professional profile.
#     """

#     input_prompt3 = """
#     You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
#     Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
#     the job description. First, the output should come as a percentage, then keywords missing, and last, final thoughts.
#     """

#     input_prompt4 = """
#     As an expert in resume optimization and keyword analysis, review the provided resume and job description.
#     Identify key keywords and phrases that are missing from the resume but are critical for the job role.
#     Provide a detailed analysis and suggest improvements to ensure the resume is optimized for ATS and increases the chances of selection.
#     """

#     input_prompt5 = """
#     As a professional resume consultant, analyze the provided resume and suggest formatting improvements.
#     Focus on layout, design, font usage, and overall readability to make the resume more appealing to hiring managers and ATS.
#     """

#     input_prompt6 = """
#     You are an experienced recruiter. Review the provided cover letter and provide feedback.
#     Highlight strengths and suggest improvements to make the cover letter more compelling and aligned with the job description.
#     """

#     input_prompt7 = """
#     As a career coach with extensive experience in interview preparation, provide tips for the candidate.
#     Focus on common interview questions, behavioral questions, and role-specific technical questions. Provide strategies for effective responses.
#     """

#     input_prompt8 = """
#     As an HR expert with knowledge of industry standards, analyze the provided resume and job description.
#     Suggest a realistic salary range based on the candidate's experience, skills, and the job market. Provide reasoning for the suggested range.
#     """

#     input_prompt9 = """
#     As a career advisor, review the provided resume and job description. Based on the candidate's experience and skills,
#     suggest potential career paths and opportunities for advancement. Provide insights on industry trends and growth areas.
#     """

#     input_prompt10 = """
#     As a professional career coach with expertise in soft skills development, review the provided resume and job description.
#     Evaluate the candidate's soft skills and provide feedback on areas such as communication, teamwork, leadership, and problem-solving.
#     Suggest ways to highlight and improve these skills.
#     """

#     input_prompt11 = """
#     As a LinkedIn optimization expert, review the provided resume and job description. Provide recommendations to optimize
#     the candidate's LinkedIn profile to align with the job description. Focus on profile completeness, keyword usage, and engagement strategies.
#     """

#     input_prompt12 = """
#     As a networking expert, provide tips and strategies for the candidate to effectively network within their industry.
#     Suggest ways to build professional relationships, leverage social media, attend industry events, and utilize networking platforms.
#     """

#     input_prompt13 = """
#     As a technical skill evaluator, analyze the provided resume and job description.
#     Identify any technical skill gaps that may exist and provide recommendations on how the candidate can bridge these gaps through training or practical experience.
#     """

#     input_prompt14 = """
#     As a project management expert, review the provided resume and job description.
#     Evaluate the candidate's project experience and provide feedback on how effectively they have demonstrated their project management skills.
#     Suggest ways to enhance the presentation of their project experiences.
#     """

#     input_prompt15 = """
#     As a career development specialist, review the provided resume and job description.
#     Recommend relevant certifications and courses that the candidate can pursue to enhance their qualifications and align better with the job requirements.
#     """

#     input_prompt16 = """
#     As an industry analyst, review the provided resume and job description.
#     Provide insights into industry-specific trends, challenges, and opportunities that the candidate should be aware of.
#     Suggest ways to leverage these insights to enhance their career prospects.
#     """

#     input_prompt17 = """
#     As a work-life balance coach, review the provided resume and job description.
#     Provide tips and strategies for the candidate to maintain a healthy work-life balance while pursuing their career goals.
#     Focus on time management, stress reduction, and personal well-being.
#     """

#     input_prompt18 = """
#     As a remote work consultant, evaluate the provided resume and job description.
#     Assess the candidate's suitability for remote work based on their skills, experience, and work habits.
#     Provide recommendations on how to improve their readiness for remote work opportunities.
#     """

#     # Handle button clicks
#     if submit1:
#         handle_submit(uploaded_file, input_prompt1, input_text, "Please upload the resume")
#     elif submit2:
#         handle_submit(uploaded_file, input_prompt2, input_text, "Please upload the resume")
#     elif submit3:
#         handle_submit(uploaded_file, input_prompt3, input_text, "Please upload the resume")
#     elif submit4:
#         handle_submit(uploaded_file, input_prompt4, input_text, "Please upload the resume")
#     elif submit5:
#         handle_submit(uploaded_file, input_prompt5, input_text, "Please upload the resume")
#     elif submit6:
#         cover_letter_text = st.text_area("Paste your cover letter here:", key="cover_letter")
#         if cover_letter_text:
#             response = get_gemini_response(input_text, [{"mime_type": "text/plain", "data": cover_letter_text}], input_prompt6)
#             st.subheader("The Response is")
#             st.write(response)
#         else:
#             st.write("Please provide a cover letter for review")
#     elif submit7:
#         handle_submit(uploaded_file, input_prompt7, input_text, "Please upload the resume")
#     elif submit8:
#         handle_submit(uploaded_file, input_prompt8, input_text, "Please upload the resume")
#     elif submit9:
#         handle_submit(uploaded_file, input_prompt9, input_text, "Please upload the resume")
#     elif submit10:
#         handle_submit(uploaded_file, input_prompt10, input_text, "Please upload the resume")
#     elif submit11:
#         handle_submit(uploaded_file, input_prompt11, input_text, "Please upload the resume")
#     elif submit12:
#         handle_submit(uploaded_file, input_prompt12, input_text, "Please upload the resume")
#     elif submit13:
#         handle_submit(uploaded_file, input_prompt13, input_text, "Please upload the resume")
#     elif submit14:
#         handle_submit(uploaded_file, input_prompt14, input_text, "Please upload the resume")
#     elif submit15:
#         handle_submit(uploaded_file, input_prompt15, input_text, "Please upload the resume")
#     elif submit16:
#         handle_submit(uploaded_file, input_prompt16, input_text, "Please upload the resume")
#     elif submit17:
#         handle_submit(uploaded_file, input_prompt17, input_text, "Please upload the resume")
#     elif submit18:
#         handle_submit(uploaded_file, input_prompt18, input_text, "Please upload the resume")

# def handle_submit(uploaded_file, input_prompt, input_text, error_message):
#     """
#     Handle the submit action for various buttons.
#     """
#     if uploaded_file:
#         pdf_parts = input_pdf_setup(uploaded_file)
#         response = get_gemini_response(input_text, pdf_parts, input_prompt)
#         st.subheader("The Response is")
#         st.write(response)
#     else:
#         st.write(error_message)

# if __name__ == "__main__":
#     main()





























# # from dotenv import load_dotenv

# # load_dotenv()
# # import base64
# # import streamlit as st
# # import os
# # import io
# # from PIL import Image 
# # import pdf2image
# # import google.generativeai as genai

# # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # def get_gemini_response(input,pdf_cotent,prompt):
# #     model=genai.GenerativeModel('gemini-1.5-flash')
# #     response=model.generate_content([input,pdf_content[0],prompt])
# #     return response.text

# # def input_pdf_setup(uploaded_file):
# #     if uploaded_file is not None:
# #         ## Convert the PDF to image
# #         images=pdf2image.convert_from_bytes(uploaded_file.read())

# #         first_page=images[0]

# #         # Convert to bytes
# #         img_byte_arr = io.BytesIO()
# #         first_page.save(img_byte_arr, format='JPEG')
# #         img_byte_arr = img_byte_arr.getvalue()

# #         pdf_parts = [
# #             {
# #                 "mime_type": "image/jpeg",
# #                 "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
# #             }
# #         ]
# #         return pdf_parts
# #     else:
# #         raise FileNotFoundError("No file uploaded")

# # ## Streamlit App

# # st.set_page_config(page_title="ATS Resume EXpert")
# # st.header("ATS Tracking System")
# # input_text=st.text_area("Job Description: ",key="input")
# # uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


# # if uploaded_file is not None:
# #     st.write("PDF Uploaded Successfully")


# # submit1 = st.button("Tell Me About the Resume")

# # submit2 = st.button("How Can I Improvise my Skills")

# # submit3 = st.button("Percentage match")
# # submit4 = st.button("what are the keywords that are missing")


# # input_prompt1 = """
# #  You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
# #   Please share your professional evaluation on whether the candidate's profile aligns with the role. 
# #  Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# # """

# # input_prompt3 = """
# # You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
# # your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
# # the job description. First the output should come as percentage and then keywords missing and last final thoughts.
# # """

# # if submit1:
# #     if uploaded_file is not None:
# #         pdf_content=input_pdf_setup(uploaded_file)
# #         response=get_gemini_response(input_prompt1,pdf_content,input_text)
# #         st.subheader("The Repsonse is")
# #         st.write(response)
# #     else:
# #         st.write("Please uplaod the resume")

# # elif submit3:
# #     if uploaded_file is not None:
# #         pdf_content=input_pdf_setup(uploaded_file)
# #         response=get_gemini_response(input_prompt3,pdf_content,input_text)
# #         st.subheader("The Repsonse is")
# #         st.write(response)
# #     else:
# #         st.write("Please uplaod the resume")

