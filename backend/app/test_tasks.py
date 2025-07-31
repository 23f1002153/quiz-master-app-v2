from app.tasks1 import addition

result = addition.delay(10, 5)
print("Task dispatched. Task ID:", result.id)