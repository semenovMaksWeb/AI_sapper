schema = {
    "0-0": {
        "x": 0,
        "y": 0,
        "val": None
    },
    "0-1": {
        "x": 1,
        "y": 0,
        "val": 1
    },
}

for value in schema.items():
    print(value)
    pass


print(schema.get("0-1"))