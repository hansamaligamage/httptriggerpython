import logging

import azure.functions as func

def main(req: func.HttpRequest, outputqueue: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    order = req.params.get('order')
    location = req.params.get('location')
    
    if not order:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            order = req_body.get('order')
            location = req_body.get('location')
                      
    if order and location:
        outputqueue.set(order + ' to ' + location)
        return func.HttpResponse(f"New order is recieved : {order + ' to ' + location}!")

    else:
        return func.HttpResponse(
             "Please pass a order item and location on the query string or in the request body",
             status_code=400
        )
