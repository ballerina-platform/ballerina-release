import ballerinax/jdbc;
import ballerina/io;
import ballerina/sql;
import ballerina/transactions;

jdbc:Client testDB = new({
   url: "jdbc:h2:file:./local-transactions/Testdb",
   username: "root",
   password: "root"
});

public function main(string... args) returns error? {
   // Create the tables
   var ret = testDB->update("CREATE TABLE CUSTOMER (
       ID INTEGER, NAME VARCHAR(30))");

   ret = testDB->update("CREATE TABLE SALARY (ID INTEGER,
       MON_SALARY FLOAT)");

   // Update two tables within a transaction
   transaction with retries = 4 {
       var result = testDB->update("INSERT INTO CUSTOMER(
           ID,NAME) VALUES (1, 'Anne')");
       var result2 = testDB->update("INSERT INTO SALARY
           (ID, MON_SALARY) VALUES (1, 2500)");

       if (result2 is sql:UpdateResult) {
           if (result2.updatedRowCount == 0) {
               abort;
           }
       }
   } onretry {
       io:println("Retrying transaction");
   } committed {
       string transactionId = transactions:getCurrentTransactionId();
       io:println("Transaction: " + transactionId + " committed");
   } aborted {
       string transactionId = transactions:getCurrentTransactionId();
       io:println("Transaction: " + transactionId + " aborted");
   }

   check testDB.stop();
}

function handleUpdate(int|error returned, string message) {
   if (returned is int) {
       io:println(message + " status: " + returned);
   } else {
       io:println(message + " failed: " + returned.reason());
   }
}
