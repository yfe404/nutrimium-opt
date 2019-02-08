from scipy.optimize import minimize


def get_ingredients():

    ingredients = [
        {
	    "name": "Beurre de cacahuètes",
	    "quantity": 100,
	    "unit": "g",
	    "calories": 592,
	    "proteins": 22.4,
	    "carbohydrates": 21,
	    "fats": 51.5,
            "price": 2.4
        }, {
	    "name": "Myrtilles",
	    "quantity": 100,
	    "unit": "g",
	    "calories": 70.5,
	    "proteins": 1,
	    "carbohydrates": 15.5,
	    "fats": 0.5,
            "price": 0.9
        }, {
	    "name": "Framboises",
	    "quantity": 100,
	    "unit": "g",
	    "calories": 36,
	    "proteins": 1,
	    "carbohydrates": 8,
	    "fats": 0,
            "price": 1.1
        }, {
	    "name": "Pomme",
	    "quantity": 100,
	    "unit": "g",
	    "calories": 54,
	    "proteins": 0.3,
	    "carbohydrates": 12,
	    "fats": 0.3,
            "price": 0.05
        }, {
	    "name": "Graines de courge",
	    "quantity": 100,
	    "unit": "g",
	    "calories": 553,
	    "proteins": 29,
	    "carbohydrates": 15,
	    "fats": 46.7,
            "price": 2.2
        }, {
	    "name": "Flocons de soja",
	    "quantity": 100,
	    "unit": "g",
	    "calories": 347,
	    "proteins": 37.3,
	    "carbohydrates": 3.1,
	    "fats": 20.6,
            "price": 1.0
        }]
    
    return ingredients


def get_target():
    target = {
	"proteins": 30,
	"carbohydrates": 0,
	"fats": 0,
	"calories": 600
    }

    return target


def get_price(quantities):
    ingredients = get_ingredients()
    return sum([ingredients[i]["price"]*quantities[i] for i in range(len(ingredients))])

def evaluate(quantities):
    utility = 0
    ingredients = get_ingredients()
    target = get_target()

    found = dict()
    
    for attribute in target.keys():
        found[attribute] = 0.0
        for idx, ingredient in enumerate(ingredients):
             found[attribute] += ingredient[attribute] * quantities[idx]

        if target[attribute] > 0:
            utility += abs(found[attribute] - target[attribute])
           
    print(found)
    price = get_price(quantities)
    print(price)
    return utility + price

if __name__ == "__main__":
    ingredients = get_ingredients()
    print("Using: ")
    [print (x["name"]) for x in ingredients]

    print("==============================")
    x0 = [1 for _ in range(len(ingredients))]
    bounds = [(0, None) for _ in range(len(ingredients))]

    
    print ("Initial utility: {}".format(evaluate(x0)))
    print("==============================")

    cons = (
        {'type': 'eq', 'fun': lambda x:  x[0] - 0.30},
        {'type': 'ineq', 'fun': lambda x:  x[1] - 0.4}
    )

    res = minimize(evaluate, x0=x0, method='SLSQP',  constraints=cons, bounds=bounds, options={'disp':True})

    print(res)

