"""
Requests library as client triggers cloudflare protection. Use curl.
"""

import json
import time
from pprint import pprint

command = r"""
curl --location --request POST 'https://www.autotrader.co.uk/at-graphql' \
--header 'Content-Type: application/json' \
--header 'Cookie: __cfduid=daa0eea48cfaf9d0655da4f0d6aec7b161605349136; bucket=desktop; __cf_bm=6010a3933754dfe9581f2d927612cca214a133df-1605350572-1800-Ae26zEHnbK5rs8FxdKcMg8JMD6Zer5Bh169AWL2WObtpLPYCiH5PAXj2mk54YXXsXvAKsbIuJT7fNJO6yHA+paM=' \
--data-raw '[
    {
        "operationName": "SearchFormFacetsQuery",
        "variables": {
            "advertQuery": {
                "postcode": null,
                "distance": null,
                "make": [
                    "make_variable"
                ],
                "homeDeliveryAdverts": null,
                "maxYear": "2020"
            },
            "facets": [
                "model"
            ]
        },
        "query": "query SearchFormFacetsQuery($advertQuery: AdvertQuery!, $facets: [SearchFacetName]) {\n  search {\n    adverts(advertQuery: $advertQuery) {\n      advertList {\n        totalElements\n        __typename\n      }\n      facets(facets: $facets) {\n        name\n        values {\n          name\n          value\n          count\n          selected\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
]'
"""

import os
from list_of_makes import makes

make_and_model_raw = {}
for make, _ in makes:
    print(make)
    stream = os.popen(command.replace("make_variable", make))
    time.sleep(1)
    models_json = stream.read()
    models_dict = json.loads(models_json)[0]
    pprint(models_dict)
    make_and_model_raw[make] = models_dict

make_and_model = []

for make, dictionary in make_and_model_raw.items():
    models = dictionary["data"]["search"]["adverts"]["facets"][0]["values"]
    models = [
        {
            "make": make,
            "model": model["name"],
            "count": model["count"]
        }
        for model in models
    ]
    make_and_model += models

with open("../make_and_model_clean.json", "w") as fp:
    json.dump(make_and_model, fp)
