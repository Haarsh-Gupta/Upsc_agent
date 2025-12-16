from init import initialize

pipeline = initialize()

data = {
    "image": "essay.png",
    "title": "Role of Civil Services in Indian Democracy",
    "paper": "GS2"
}

node = pipeline
while node:
    result = node.handler(data)
    node = node.edges.get(result["next"])
    data = result["data"]

print("\n--- FINAL SCORE ---\n")
print(data["evaluation"])
