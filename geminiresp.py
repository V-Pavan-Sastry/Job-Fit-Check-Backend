import google.generativeai as genai

def getResp(resumeData,jd,apiKey):
    input_prompt="""
    You are a technical HR Manager entasked with reviewing resumes for a job description.
    You will have to review the Resume and provide the following info extracted in json format with below template as reference

    "res":{
    "NAME":"name-of-the-candidate",
    "PHNO":"phone-number-of-the-candidate",
    "EMAIL":"email-of-the-candidate",
    "TOTAL_EXPERINCE":"experience-of-the-candidate-in-years",
    "PERCENTAGE_MATCH":"percentage-of-match", // Percentage that the candidate fits for the role
    "REQUIREMENT":[
    {"requirement-for-the-job":True}, //"requirement-for-the-job" may be "Experience 3yrs" or"C++" or "python" or another skills (let requirements be of 2/3 words max)
    {"requirement-for-the-job":False}  //True or False if the candidate has mentioned the same in their resume or is implied based on review
    ]
    "ADDITIONAL_SKILLS":[
    {"skill-in-resume-not-required-for-the-job":True}, //"skill-in-resume-not-required-for-the-job" may be "C++" or "python" or another skills
    {"skill-in-resume-not-required-for-the-job":False}  //True or False if its usefull for the role provided in Job Descriptionspecifically
    ],
    "QUESTIONS":['question-1','question-2'] //add min 5 questions that can be asked be asked in interview based on the candidates rresume and job requirement
    }


    and if not found return empty "" or [] respectively
    """
    genai.configure(api_key=apiKey)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(input_prompt+"\nJOB DESCRIPTION\n"+jd+"RESUME\n"+resumeData)
    print(response.text)
    print(response.prompt_feedback)
    return response.text