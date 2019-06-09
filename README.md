# Create a Http Trigger function in Python

This code sample is built on Python 3.6 using Visual Studio Code IDE. It's going to create a very simple order processing system with a Azure Queue storage account.

# Before running the solution

1. You have to create a Python virtual environment to run the project, click on Create virtual environment button
![Create a Python virtual environmenr](https://github.com/hansamaligamage/httptriggerpython/blob/master/images/create-virtual-environment.png)

2. You have to install required references to the project
![Install required dependencies](https://github.com/hansamaligamage/httptriggerpython/blob/master/images/restore-packages.png)


  3.Then you have to install the binding extensions to the project 
![Install binding extensions](https://github.com/hansamaligamage/httptriggerpython/blob/master/images/install-binding-extensions.png)

# Sample code files
You can find the main python file that logs order item to a queue when a http request comes

```
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
```

You can see the function.json file has output queue storage binding
```
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": [
        "get",
        "post"
      ]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    },
    {
      "name": "outputqueue",
      "type": "queue",
      "direction": "out",
      "connection": "MyStorageConnectionString",
      "queueName": "itemsqueue"
}
  ]
}
```

You have to add the connectionstring to the queue storage as below,
```
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "MyStorageConnectionString" : "DefaultEndpointsProtocol=https;AccountName='';AccountKey='';EndpointSuffix=core.windows.net"
  }
}
```

If you want to know more, go through this post [Azure Functions for Python Developers](http://hansamaligamage.blogspot.com/2019/06/azure-functions-for-python-developers.html) 
