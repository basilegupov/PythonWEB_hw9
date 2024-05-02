from models import Author, Quote


def search_quotes(command):
    if command.startswith("name:"):
        author_name = command.split(":")[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.to_json())
        else:
            print("Автора не знайдено")
    elif command.startswith("tag:"):
        tag = command.split(":")[1].strip()
        quotes = Quote.objects(tags=tag)
        for quote in quotes:
            print(quote.to_json())
    elif command.startswith("tags:"):
        tags = command.split(":")[1].strip().split(",")
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            print(quote.to_json())
    else:
        print("Невідома команда")


if __name__ == "__main__":
    while True:
        command = input("Введіть команду: ")
        if command == "exit":
            break
        search_quotes(command)
