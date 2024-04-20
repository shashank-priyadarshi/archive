package main

import (
	// fmt is a standard package provided by Golang
	"fmt" // Package fmt implements formatting operations on the console like printing, reading input, etc

	// These are custom packages defined by us
	"github.com/shashank-priyadarshi/training/calculator/add"      // Importing add package from calculator
	"github.com/shashank-priyadarshi/training/calculator/divide"   // Importing divide package from calculator
	"github.com/shashank-priyadarshi/training/calculator/multiply" // Importing multiply package from calculator
	"github.com/shashank-priyadarshi/training/calculator/subtract" // Importing subtract package from calculator
)

// Calculator
// Add, Subtract, Multiply, Divide
func main() {
	a := add.Add(1, 2)
	fmt.Println("Adding: ", a) // Writing to the console

	a = subtract.Subtract(1, 2)
	fmt.Println("Subtracting: ", a)

	a = multiply.Multiply(1, 2)
	fmt.Println("Multiplying: ", a)

	a = divide.Divide(1, 2) // It will print 0, not 0.5, Data types are important
	fmt.Println("Dividing: ", a)

	// It will cause runtime error, not compile time error
	a = divide.Divide(1, 0) // It will panic, because we are dividing by 0
	fmt.Println("Dividing: ", a)
}
