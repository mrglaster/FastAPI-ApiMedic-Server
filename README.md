### FastAPI ApiMedic Server
A Python server (FastAPI) that simplifies the work with the ApiMedic service. Send simpler requests to your server and get the result from the service. This server uses client code from the [priaid-eHealth project](https://github.com/priaid-eHealth/symptomchecker)

### How to use?

1) Install required dependencies with command 

``` pip install -r requirements.txt```

2) Add your auth data to cfg/config.py

```
username = "USE YOUR OWN!" # Here enter your API user name
password = "USE YOUR OWN!" # Here enter your API password
priaid_authservice_url = "https://authservice.priaid.ch/login"
priaid_healthservice_url = "https://healthservice.priaid.ch"
language = "en-gb"
pritnRawOutput = False
```

3) Run the server
4) Profit!

### Links

1) [priaid-eHealth project](https://github.com/priaid-eHealth/symptomchecker)
2) [Symptom Checker API](https://apimedic.com/)
3) [FastAPI](https://fastapi.tiangolo.com/)



