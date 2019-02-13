import json


def main(event, context):

    try:
        data = json.loads(event['body'])
        print(data)
    
        body = {
            "quantities": {"x1": 0.8, "x2": 0.7},
            "macros": {"a": 10, "b": 32},
            "price": 42.00
        }

        response = {
            "statusCode": 200,
            "headers": {
	        "Access-Control-Allow-Origin": "*",
	        "Access-Control-Allow-Credentials": True
            },
            "body": body
        }
    

        return response
    
    except Exception as err:
        response = {
            "statusCode": 500,
            "headers": {
	        "Access-Control-Allow-Origin": "*",
	        "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({"message": str(err)})
        }
        
    return response
