from modules import checker_client
from cfg import config
import uvicorn
import os
from fastapi import FastAPI, Request

# Init section
app = FastAPI()
username = config.username
password = config.password
authUrl = config.priaid_authservice_url
healthUrl = config.priaid_healthservice_url
language = config.language
api_medic_client = checker_client.DiagnosisClient(username=username, password=password, auth_service_url=authUrl,
                                                  health_service_url=healthUrl, language=language)


@app.get("/symptoms")
async def get_symptoms():
    return {"symptoms": api_medic_client.load_symptoms()}


@app.get("/issues")
async def get_issues():
    return {"issues": api_medic_client.load_issues()}


@app.post("/issue_info")
async def get_issue_info(info: Request):
    req_info = await info.json()
    issue_id = req_info["issue_id"]
    return {"information": api_medic_client.load_issue_info(issue_id)}


@app.post("/identify_disease")
async def identify_disease(info: Request):
    req_info = await info.json()
    potential_diseases = req_info["symptoms"]
    gender = req_info["gender"]
    year_of_birth = req_info["year_of_birth"]
    return {"result": api_medic_client.loadDiagnosis(potential_diseases, gender, year_of_birth)}


@app.get("/red_flag")
async def get_red_flag(info: Request):
    req_info = await info.json()
    symptom_id = req_info['symptom_id']
    return {"result": api_medic_client.load_red_flag(symptom_id)}


@app.get("/body_sublocations")
async def get_body_sublocations(info: Request):
    req_info = await info.json()
    body_location_id = req_info["body_sublocation"]
    return {"result": api_medic_client.load_body_sublocation(body_location_id)}


@app.post("/get_specialisations")
async def get_specialisations(info: Request):
    req_info = await info.json()
    selected_symptoms = req_info["symptoms"]
    gender = req_info["gender"]
    year_of_birth = req_info["year_of_birth"]
    return {"result": api_medic_client.load_specialisations(selectedSymptoms=selected_symptoms, gender=gender,
                                                            yearOfBirth=year_of_birth)}


def main():
    uvicorn.run(f"{os.path.basename(__file__)[:-3]}:app", log_level="info")


if __name__ == '__main__':
    main()
