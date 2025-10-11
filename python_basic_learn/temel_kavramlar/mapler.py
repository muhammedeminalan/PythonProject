sozluk = {"merhaba": "hello", "kitap": "book", "defter": "notebook"}
print(sozluk["merhaba"])  # Output: hello
print(sozluk.get("kitap"))  # Output: book
print(sozluk.keys())  # Output: dict_keys(['merhaba', 'kitap', 'defter'])
print(sozluk.values())  # Output: dict_values(['hello', 'book', 'notebook'])
print(sozluk.items())  # Output: dict_items([('merhaba', 'hello'), ('kitap', 'book'), ('defter', 'notebook')])
sozluk["kalem"] = "pen"
sozluk.pop("kitap")
print(sozluk)
