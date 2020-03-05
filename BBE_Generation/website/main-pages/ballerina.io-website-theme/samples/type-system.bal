any anything; 
int integer = 0;
float floatingPoint = 0.0;
boolean bool = true;
string hi = "hello";
byte[] byteArr = hi.toByteArray("UTF-8");

json j = { a: "hello", b: 5 };

xml x = xml `<ballerina>
                <supports>XML natively</supports>
             </ballerina>`;

string[] stringArray = ["hi", "there"];
int[][] arrayOfArrays = [[1,2],[3,4]];
json|xml|string unionType;
(string, int) tuple = ("hello", 5);
() n = (); // the empty tuple acts as "null"
string|error stringOrError = "this is a union type";
int? optionalInt = 5; // an int value or no value
map<boolean> myMap = { "ballerina": true };

type myRecord record { string a; int b; };

type myObject object {
    public string p;
    private int q;
    function __init(string p, int q) {
        self.p = p;
        self.q = q;
    }
    function getX() returns (string) {
        return self.p;
    }
};