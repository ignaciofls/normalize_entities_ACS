import logging
import string
from collections import Counter,OrderedDict
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request')
    try:
        req_body = req.get_json()['values']
    except ValueError:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )
    if req_body:
        result = brains(req_body)
        logging.info(result)
        return func.HttpResponse(json.dumps(result), mimetype="application/json")  
    else:
        return func.HttpResponse("Invalid json body",status_code=555)              

def brains(json_data): 
    myheaders = []
    for val in json_data:
        text = val['data']['text']
        record_id = val['recordId']
        logging.info(text)
        if text !=[] :
            json_output = {"recordId": record_id, "data": {"text": rank(text)}}
            myheaders.append(json_output)
        else:  # when no keyPhrase is found
            json_output = {"recordId": record_id, "data": {"text": []}}
            myheaders.append(json_output)
            #return func.HttpResponse("Invalid json data/text structure inside json",status_code=555)     
    output = {"values": myheaders}
    logging.info(json.dumps(output, indent=2))
    return output

def rank (ListofStrings):
    z = []
    for e in ListofStrings:
        e = e.replace('.', '')
        z.append(e)
    x = [element.title() for element in z] ; z
    y = list(dict.fromkeys((sorted(x, key=Counter(x).get, reverse=True))))
    y = y[:10] # Limit it to the top 10 because that's what is rendered in the facet UI
    return y

'''
Use this string to test input
{"values": [
      {
        "recordId": "a1",
        "data":
           {
            "text": ["My.key1","MYKEY1","MyKey1","My.Key.1","Mykey2","Mykey3","My.key.1","Mykey5", "Mykey6","Mykey7","Mykey8","Mykey9"]
           }
      } 
    ]
}

Output should be like: {"values": [{"recordId": "a1", "data": {"text": ["Mykey1", "Mykey2", "Mykey3", "Mykey5", "Mykey6", "Mykey7", "Mykey8", "Mykey9"]}}]}"
'''