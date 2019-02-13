import json
import numpy as np
from scipy.optimize import minimize


def get_price(ingredients, quantities):
    """Return the price of a recipe given the ingredients and the 
       associated quantities.
    """
    return sum([ingredients[i]["price"]*quantities[i] for i in range(len(ingredients))])

def get_macros(quantities, target, ingredients):
    """Return the macros of a recipe given the ingredients and 
       the associated quantities.
    """
    macros = dict()
    for attribute in target.keys():
        macros[attribute] = 0.0
        for idx, ingredient in enumerate(ingredients):
             macros[attribute] += ingredient[attribute] * quantities[idx]
        macros[attribute] = int(macros[attribute])
    return macros
    

def evaluate(quantities, ingredients):
    """Objective function to minimize"""
    price = get_price(ingredients, quantities)
    price = np.round(price, 2)
    return price


def main(event, context):

    try:

        ## Parsing body request to extract recipe and target profile
        data = json.loads(event['body'])
        print(data)

        ingredients = data['ingredients']
        target = data['target']
        
        ## Linear Solver Settings
        ### tolerance of the constraints: C +/- epsilon
        epsilon = 25/2 

        ### initial solution
        x0 = [1 for _ in range(len(ingredients))]

        ### quantities must be positive or zero
        bounds = [(0, None) for _ in range(len(ingredients))]

        ### Constraints on the target profile (only considering
        ### calories and proteins for now
        cons = (
        {'type': 'ineq', 'fun':
         lambda x: sum([x[i]*ingredients[i]["calories"] for i in range(len(ingredients))]) - epsilon - target["calories"]},
        {'type': 'ineq', 'fun': lambda x: -sum([x[i]*ingredients[i]["calories"] for i in range(len(ingredients))]) - epsilon + target["calories"]},
        {'type': 'ineq', 'fun': lambda x: -sum([x[i]*ingredients[i]["proteins"] for i in range(len(ingredients))]) + target["proteins"]}
        )

        res = minimize(evaluate, x0=x0, args=(ingredients), method='SLSQP',  constraints=cons, bounds=bounds, options={'disp':False})

        print(res)

        quantities = [np.round(x, 2) for x in res.x]
        price = res.fun
        macros = get_macros(quantities, target, ingredients)
        
        body = {
            "quantities": quantities,
            "macros": macros,
            "price": price
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
