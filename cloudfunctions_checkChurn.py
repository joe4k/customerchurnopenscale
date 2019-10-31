#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
import requests, json
import ast

def getToken(apikey):
    # Get an IAM token from IBM Cloud
    url     = "https://iam.bluemix.net/oidc/token"
    headers = { "Content-Type" : "application/x-www-form-urlencoded" }
    data    = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    IBM_cloud_IAM_uid = "bx"
    IBM_cloud_IAM_pwd = "bx"
    response  = requests.post( url, headers=headers, data=data, auth=( IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd ) )
    iam_token = response.json()["access_token"]
    return iam_token

def predictChurn(iam_token,ml_instance_id,scoring_url,flds,vals):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token, 'ML-Instance-ID': ml_instance_id}
    
    payload_scoring = {"input_data": [{"fields": flds, "values": vals}]}
    response_scoring = requests.post(scoring_url, json=payload_scoring, headers=header)
    churn = json.loads(response_scoring.text)
    return churn
    
def main(dict):
    apikey = dict['apikey']
    ml_instance_id = dict['ml_instance_id']
    scoring_url = dict['scoring_url']
    flds_array = ast.literal_eval(dict['fields'])
    vals_array = ast.literal_eval(dict['values'])
    
    iam_token = getToken(dict['apikey'])
    churn_prediction = predictChurn(iam_token,ml_instance_id,scoring_url,flds_array,vals_array)
    
    return churn_prediction
