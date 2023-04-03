from flask import Flask, request
from random import choice, randint

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

about_me = {
   "name": "Владимир",
   "surname": "C",
   "email": "admin@admin.ru"
}

quotes = [
   {
       "id": 3,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
   },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
   },
   {
       "id": 6,
       "author": "Mosher’s Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
   },
   {
       "id": 8,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так."
   },

]

for quota in quotes:
   quota.update({'rating':randint(1,5)})


@app.route("/about")
def about():
   return about_me


@app.route("/")
def hello_world():
   return "Hello, World!"

#Сериализация list -> str
@app.route("/quotes")
def get_quotes():
   return quotes


@app.route("/quotes/<int:id>")
def get_qoutes(id:int):

   for qouta in quotes:
    if qouta['id'] == id:
        return qouta
    
    return f"Quote with id={id} not found", 404


@app.route("/quotes/random", methods=["GET"])
def get_random_qouta():
   return choice(quotes) 


@app.route("/quotes/count")
def get_counts():
   return {
      "count": len(quotes)
   }


@app.route("/quotes", methods=['POST'])
def create_quote():
   new_quote = request.json
   rating = new_quote.setdefault('rating',1)
   if 0 == rating > 5:
      new_quote["rating"] = 1
   last_quote = quotes[-1]
   new_id = last_quote["id"]+1
   new_quote["id"] = new_id
   quotes.append(new_quote)
   print(new_quote)
   return new_quote, 201


@app.route("/quotes/<int:id>", methods=['PUT'])
def edit_quote(id:int):
   new_data = request.json

   if new_data["rating"] and (0 == new_data["rating"] or  new_data["rating"]  > 5):
      new_data["rating"] = 1
   
   for quote in quotes:
      if quote['id'] == id:
        quote.update(new_data.items())
        return quote, 200
      
      return f"цитата с id {id} не найдена", 404


@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id:int):
   for el in range(len(quotes)):
    if quotes[el]['id']==id:
       quotes.pop(el)
       return f"Quote with id {id} is deleted.", 200
    
    return f"цитата с id {id} не найдена", 404

@app.route("/quotes/filter", methods=["GET"])
def set_filter():
   args = request.args.to_dict()
   params = args.keys()
   for quota in quotes:
      for param in params:
         if quota[param] == args[param]:
            pass
        
      

   return args




if __name__ == "__main__":
   app.run(debug=True)
