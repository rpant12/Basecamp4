import requests
import pandas as pd

# Your refresh token pulled from your account
refreshtoken = '8kSsMlJYXs-bV2uJsGxmvMgF-7A69txHjXy2-nWTodo'

# Variables
orgid = 31088
reportId = 1519
whereToOutput = 'PLREDeviceAllocations.csv'

# Configure everything to get your access token for authentication
headers = {
    'Accept': 'Application/Json'
}
body = {
    'grant_type': 'refresh_token',
    'refresh_token': refreshtoken
}

uri = "https://login.flexera.com/oidc/token"
response = requests.post(uri, headers=headers, data=body)
accesstoken = response.json()

# Now that we have your access token, configure your bearer token and do the actual API call
token = accesstoken['access_token']
btoken = f"Bearer {token}"

headers = {
    'Accept': 'Application/Json',
    'Authorization': btoken
}

uri = f"https://beta.api.flexera.com/fnms/v1/orgs/{orgid}/reports/{reportId}/execute"
response = requests.get(uri, headers=headers)
result = response.json()

# Convert the result values to a DataFrame and save to CSV
df = pd.DataFrame(result['values'])

NextPage = result.get('nextPage')
while NextPage:
    uri = f"https://beta.api.flexera.com{NextPage}"
    response = requests.get(uri, headers=headers)
    result = response.json()
    df_next = pd.DataFrame(result['values'])
    df = pd.concat([df, df_next])
    NextPage = result.get('nextPage')

df.to_csv(whereToOutput)