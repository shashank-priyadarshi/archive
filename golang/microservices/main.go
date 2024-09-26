package main // required, cannot be multiple unique package in single directory

// Go automatically sort imports
// And, removes unused imports
// To retain an unused import, alias it with `_`
// Other custom import aliases are also allowed
// Importing functions from `package main` is disallowed
// Only exported functions from a package can be imported in another package, i.e. functions starting in capital case
import (
	_ "bufio"
	"fmt"
	_ "strings"

	_ "github.com/mattn/go-sqlite3" // go get github.com/mattn/go-sqlite3
	demo "github.com/shashank-priyadarshi/archive/golang/microservices/pkg"
)

func init() {
	// pre requisite setup
}

func main() {
	fmt.Println("hello from github.com/shashank-priyadarshi/archive/golang/microservices")

	demo.ExportedFunc()
	// demo.unexportedFunc() using unexported func not allowed

	a := demo.Animal{
		Something: "something",
	}
	fmt.Println(a.Something)
	// fmt.Println(a.name) using unexported struct property not allowed
	a.Class1()
	// a.class1() using unexported method not allowed

	fmt.Println(a)
	// b := demo.animal{} using unexported type not allowed

}
