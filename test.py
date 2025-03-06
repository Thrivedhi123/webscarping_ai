import spacy
import json
from scrape import scrape_website, clean_body_content, extract_body_content

# Load pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

# Define function to extract structured university data
def extract_entities(text):
    doc = nlp(text)
    extracted_data = {
        "University_Id": None,  # Unique ID can be assigned separately
        "University_Name": None,
        "University_Website": None,
        "University_Logo_Url": None,
        "University_Type": None,
        "Acceptance_Rate": None,
        "Student_To_Faculty_Ratio": None,
        "Available_Programs": [],
        "Available_Scholarships": [],
        "Location": None,
        "Country": None,
        "QS_University_Ranking": None,
        "Times_Ranking": None,
        "Shanghai_Ranking": None,
        "search_vector": None,
        "Contact": {
            "Admissions_Email": None,
            "Admissions_Phone": None,
            "Admissions_Address": None
        },
        "Accreditation": {
            "University_Accreditation": None
        },
        "StudentDemographics": {
            "University_Student_Demographics": None,
            "University_Gender_Diversity": None,
            "University_International_Student_Percentage": None,
            "University_Number_of_Applicants": None,
            "University_Number_of_Enrolled_Students": None,
            "University_Number_of_Admissions": None
        },
        "FacultyResearchImpacts": {
            "University_H_Index": None,
            "University_Citations": None,
            "University_Citations_Per_Publication": None,
            "University_Citations_Per_Faculty": None,
            "University_Citations_Per_Document": None
        },
        "CampusFacilities": {
            "University_Library": None,
            "University_Sports_Facilities": None,
            "University_Student_Services": None,
            "University_Accommodation": None,
            "University_Health_Services": None
        }
    }

    # Extract Named Entities
    for ent in doc.ents:
        if ent.label_ == "ORG":
            extracted_data["University_Name"] = ent.text
        elif ent.label_ == "GPE":
            extracted_data["Country"] = ent.text
        elif ent.label_ == "PERCENT":
            extracted_data["Acceptance_Rate"] = ent.text
        elif ent.label_ == "CARDINAL":
            extracted_data["StudentDemographics"]["University_Number_of_Enrolled_Students"] = ent.text
        elif ent.label_ == "LOC":
            extracted_data["Location"] = ent.text
        elif ent.label_ == "URL":
            extracted_data["University_Website"] = ent.text
        elif ent.label_ == "RANK":
            extracted_data["QS_University_Ranking"] = ent.text  # Assuming ranking entity exists
        elif ent.label_ == "EMAIL":
            extracted_data["Contact"]["Admissions_Email"] = ent.text
        elif ent.label_ == "PHONE":
            extracted_data["Contact"]["Admissions_Phone"] = ent.text

    return extracted_data

# Scrape website and clean data
text = scrape_website("https://www.topuniversities.com/world-university-rankings")
body_content, links, img_links = extract_body_content(text)
clean_content = clean_body_content(body_content)

# Extract structured university data
extracted_info = extract_entities(clean_content)

# Convert extracted data to JSON format
json_output = json.dumps(extracted_info, indent=4)
print(json_output)
