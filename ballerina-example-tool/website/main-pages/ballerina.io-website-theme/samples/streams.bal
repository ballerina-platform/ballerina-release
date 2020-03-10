import ballerina/io;
import ballerina/runtime;

type StatusCount record {
    string status;
    int totalCount;
};

type Teacher record {
    string name;
    int age;
    string status;
    string school;
};

stream<StatusCount> filteredCountStream = new;
stream<Teacher> teacherStream = new;

function testAggregationQuery () {

    forever {
        from teacherStream where teacherStream.age > 18
                window lengthBatch(3)
        select teacherStream.status, count() as totalCount
        group by teacherStream.status
        having totalCount > 1
        => (StatusCount[] statusCounts) {
            foreach var st in statusCounts {
                filteredCountStream.publish(st);
            }
        }
    }
}

public function main (string... args) {

    testAggregationQuery();
    filteredCountStream.subscribe(printStatusCount);

    Teacher t1 = { name:"Jane",
                   age:25,
                   status:"single", 
                   school:"MIT"
                 };
    Teacher t2 = { name:"Shareek",
                   age:33,
                   status:"single",
                   school:"UCLA"
                 };
    Teacher t3 = {
                   name:"Sue",
                   age:45,
                   status:"married",
                   school:"Stanford"
                 };

    teacherStream.publish(t1);
    teacherStream.publish(t2);
    teacherStream.publish(t3);

    runtime:sleep(2000);
}

function printStatusCount (StatusCount s) {
    io:println("Event received: status: " + 
        s.status + "; total: " + s.totalCount);
}