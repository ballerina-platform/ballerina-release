import ballerina/http;
import ballerina/io;

http:Client backendEP = new("https://ballerina.io/samples");

service store on new http:Listener(9090) {

   resource function bookDetails(http:Caller caller, http:Request req)
                                   returns error? {
       http:Response response = check backendEP->get("/bookstore.json");

       json bookStore = check response.getJsonPayload();
       json filteredBooksJson = filterBooks(bookStore, 1900);
       xml filteredBooksXml = check filteredBooksJson.toXML({});

       response.setPayload(untaint filteredBooksXml);

       check caller->respond(response);
   }
}

function filterBooks(json bookStore, int yearParam) returns json {
   json filteredBooks = {books:[]};
   int index = 0;

   json[] books = <json[]>bookStore.store.books;
   foreach json book in books {
       int|error year = int.convert(book.year);

       if (year is int) {
           if (year > yearParam) {
               filteredBooks.books[index] = book;
               index += 1;
           }
       }
   }

   return filteredBooks;
}