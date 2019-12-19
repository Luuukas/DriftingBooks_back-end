from BookModel.models import Book

def getAbout(bookname, writer, press):
    return ["https://img3.doubanio.com/view/subject/l/public/s6273530.jpg","好好笑的爱"]

def add_book(bookname, writer, press, neededcredit):
    about = getAbout(bookname, writer, press);
    book = Book(bookname=bookname, writer=writer, press=press, neededcredit=neededcredit,coverurl=about[0],description=about[1])
    book.save()
    return {"state":0}

def get_book(bookname, writer, press):
    try:
        book = Book.objects.get(bookname=bookname, writer=writer, press=press);
    except BaseException:
        return {"state":1}
    else:
        return {"state":0, "infos":[book.booid, book.bookname, book.writer, book.press ,book.neededcredit, book.coverurl, book.description]}

def get_all_books():
    list = Book.objects.all()
    books = []
    for record in list:
        books.append([record.booid, record.bookname, record.writer, record.press, record.neededcredit, record.coverurl, record.description])
    return {"state":0, "books":books}

def del_book(bookname, writer, press):
    try:
        book = Book.objects.get(bookname=bookname, writer=writer, press=press);
    except BaseException:
        return {"state":1}
    else:
        book.delete()
        return {"state":0}