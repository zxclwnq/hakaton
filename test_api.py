from requests import get, post

# Корректный запрос
print(get('http://localhost:5000/api/calls/1').json())
# Корректный запрос
new_call = {"message":"Я подвернула правую ногу. Она сильно распухла и болит.",  "address":"Москва, ул. Погодинская, 8" }
print(post('http://localhost:5000/api/calls', json=new_call).json())
# Корректный запрос
print(get('http://localhost:5000/api/calls').json())
# Некорректный запрос
print(get('http://localhost:5000/api/calls/1111').json())
# Некорректный запрос
new_call = {"message":"Я подвернула правую ногу. Она сильно распухла и болит.",  "address":"254162146514qwghg5142154126" }
print(post('http://localhost:5000/api/calls', json=new_call).json())
