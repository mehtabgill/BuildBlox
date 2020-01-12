from lib import lib

# You should avoid sharing this token,
#  and should store it in an env variable
lib = lib(token="tok_dev_K8bKg3xWy7Lq8sWR3pRACcgCYJF8FRGTzQCRPP8c3fpQ8fTBNJwDtdweToCnyCC8")

# HTML Requests, works for URLs and all HTML methods
# request = lib.http.request["@1.0.1"]
# result = request(
#   method='GET', # (required)
#   url="https://www.google.ca/" # (required)
# )




# send text message
# sms = lib.utils.sms["@1.0.11"]

# result = sms(
#   to="7785583011", # (required)
#   body="VSCodeTest" # (required)
# )

# Query mySpreadsheet
query = lib.googlesheets.query["@0.3.0"]

result = query.count(
    spreadsheetId = "mySpreadsheet",
    range="A1:D4" # (required)
)


# Delete from mySpreadsheet
# result = query.delete(
#   range="A1:A4" # (required)
# )

# Insert row in mySpreadsheet

