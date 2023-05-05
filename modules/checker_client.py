import requests
import hmac, hashlib
import base64
import json
from enum import Enum


SelectorStatus = Enum('SelectorStatus', 'Man Woman Boy Girl')


class DiagnosisClient:
    def __init__(self, username, password, auth_service_url, language, health_service_url):
        self._handle_request_arguments(username, password, auth_service_url, health_service_url, language)

        self._language = language
        self._healthServiceUrl = health_service_url
        self._token = self._load_token(username, password, auth_service_url)

    @staticmethod
    def _load_token(username, password, url):

        rawHashString = hmac.new(bytes(password, encoding='utf-8'), url.encode('utf-8'), digestmod=hashlib.md5).digest()
        computedHashString = base64.b64encode(rawHashString).decode()

        bearer_credentials = username + ':' + computedHashString
        postHeaders = {
            'Authorization': 'Bearer {}'.format(bearer_credentials)
        }
        responsePost = requests.post(url, headers=postHeaders)

        data = json.loads(responsePost.text)
        return data

    @staticmethod
    def _handle_request_arguments(username, password, authUrl, healthUrl, language):
        if not username:
            raise ValueError("Argument missing: username")

        if not password:
            raise ValueError("Argument missing: password")

        if not authUrl:
            raise ValueError("Argument missing: authServiceUrl")

        if not healthUrl:
            raise ValueError("Argument missing: healthServiceUrl")

        if not language:
            raise ValueError("Argument missing: language")

    def _load_from_web_service(self, action):
        extraArgs = "token=" + self._token["Token"] + "&format=json&language=" + self._language
        if "?" not in action:
            action += "?" + extraArgs
        else:
            action += "&" + extraArgs

        url = self._healthServiceUrl + "/" + action
        response = requests.get(url)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("----------------------------------")
            print("HTTPError: " + e.response.text)
            print("----------------------------------")
            raise

        try:
            dataJson = response.json()
        except ValueError:
            raise requests.exceptions.RequestException(response=response)

        data = json.loads(response.text)
        return data

    def load_symptoms(self):
        return self._load_from_web_service("symptoms")

    def load_issues(self):
        return self._load_from_web_service("issues")

    def load_issue_info(self, issueId):
        if isinstance(issueId, int):
            issueId = str(issueId)
        action = "issues/{0}/info".format(issueId)
        return self._load_from_web_service(action)

    def load_diagnosis(self, selectedSymptoms, gender, yearOfBirth):
        if not selectedSymptoms:
            raise ValueError("selectedSymptoms can not be empty")

        if gender != 'Male' and gender != 'Female':
            raise ValueError("Wrong gender!")

        serializedSymptoms = json.dumps(selectedSymptoms)
        action = "diagnosis?symptoms={0}&gender={1}&year_of_birth={2}".format(serializedSymptoms, gender,
                                                                              yearOfBirth)
        return self._load_from_web_service(action)

    def load_specialisations(self, selectedSymptoms, gender, yearOfBirth):
        if not selectedSymptoms:
            raise ValueError("selectedSymptoms can not be empty")
        if gender != 'Male' and gender != 'Female':
            raise ValueError("Unknown gender")
        serializedSymptoms = json.dumps(selectedSymptoms)
        action = "diagnosis/specialisations?symptoms={0}&gender={1}&year_of_birth={2}".format(serializedSymptoms,
                                                                                              gender, yearOfBirth)
        return self._load_from_web_service(action)

    def load_body_locations(self):
        return self._load_from_web_service("body/locations")

    def load_body_sublocation(self, bodyLocationId):
        action = "body/locations/{0}".format(bodyLocationId)
        return self._load_from_web_service(action)

    def load_sublocation_symptoms(self, locationId, selectedSelectorStatus):
        action = "symptoms/{0}/{1}".format(locationId, selectedSelectorStatus.name)
        return self._load_from_web_service(action)

    def load_proposed_symptoms(self, selectedSymptoms, gender, yearOfBirth):
        if not selectedSymptoms:
            raise ValueError("selectedSymptoms can not be empty")
        serializedSymptoms = json.dumps(selectedSymptoms)
        action = "symptoms/proposed?symptoms={0}&gender={1}&year_of_birth={2}".format(serializedSymptoms, gender.name,
                                                                                      yearOfBirth)
        return self._load_from_web_service(action)

    def load_red_flag(self, symptomId):
        action = "redflag?symptomId={0}".format(symptomId)
        return self._load_from_web_service(action)
