from BookModel.models import Book

def add_book(bookname, writer, press, neededcredit):
    book = Book(bookname=bookname, writer=writer, press=press, neededcredit=neededcredit)
    book.save()
    return {"state":0}

def get_book(bookname, writer, press):
    try:
        book = Book.objects.get(bookname=bookname, writer=writer, press=press);
    except BaseException:
        return {"state":1}
    else:
        return {"state":0, "infos":[book.booid, book.bookname, book.writer, book.press ,book.neededcredit]}

def get_all_books():
    list = Book.objects.all()
    books = []
    for record in list:
        books.append([record.booid, record.bookname, record.writer, record.press, record.neededcredit])
    return {"state":0, "books":books}

def del_book(bookname, writer, press):
    try:
        book = Book.objects.get(bookname=bookname, writer=writer, press=press);
    except BaseException:
        return {"state":1}
    else:
        book.delete()
        return {"state":0}