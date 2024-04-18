import base64
client_id = "FUrOrsKRSDN1su2R15l2RVMNor07PNhqUXhKhlSc"
secret = "rHu3UjgpnEavL0T3FAGOR23shtzuRCtC4jMaELqGdhtIQrta2SSyHG5JqlvuUnKbxHaLjszEH9ftDdoncpnI3irtF7LWp2XqWO2Vu0WjV3BKGq8etA1fOw5HzXoYfs00"
credential = "{0}:{1}".format(client_id, secret)
print(base64.b64encode(credential.encode("utf-8")))

# RlVyT3JzS1JTRE4xc3UyUjE1bDJSVk1Ob3IwN1BOaHFVWGhLaGxTYzpySHUzVWpncG5FYXZMMFQzRkFHT1IyM3NodHp1UkN0QzRqTWFFTHFHZGh0SVFydGEyU1N5SEc1SnFsdnVVbktieEhhTGpzekVIOWZ0RGRvbmNwbkkzaXJ0RjdMV3AyWHFXTzJWdTBXalYzQktHcThldEExZk93NUh6WG9ZZnMwMA==

# {"access_token": "Pe9YSHms8oZdMMTAO13LwebUeYhECa", "expires_in": 36000, "token_type": "Bearer", "scope": "read write groups"}