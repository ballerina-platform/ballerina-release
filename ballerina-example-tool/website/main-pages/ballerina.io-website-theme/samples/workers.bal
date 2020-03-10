import ballerina/io;

public function main(string... args) {
    // Each function consists of one or more workers which are
    // independent parallel execution code blocks
    worker w1 {
        int n = 10000000;
        int sum = 0;

        foreach var i in 1 ... n {
            sum += i;
        }

        io:println("sum of first ", n,
            " positive numbers = ", sum);
    }

    worker w2 {
        int n = 10000000;
        int sum = 0;

        foreach var i in 1 ... n {
            sum += i * i;
        }

        io:println("sum of squares of first ", n,
            " positive numbers = ", sum);
    }
}