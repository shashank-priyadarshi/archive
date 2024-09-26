package types

import (
	"fmt"
	"net/http"
	"net/url"
	"time"
)

// Statically Typed Languages: Types are static after they have been defined for a variable
// Dynamically Typed Languages: Types are dynamic, which means types of variables can change within the same scope based no value
// Following code will work in JavaScript(dynamically typed), but not in Golang(statically typed):
// var x = 0
// x = 4.3
// x = "Shashank"

// Scalar data types: Numbers and Strings
// Vector data types: Arrays, Slices and Maps
// Custom types
// Composite data type: Struct
// any/interface

func types() {
	// Declaration: creating a new name to be used as a variable
	// Defining: defining some property of the variable like a data type
	// Initializing: putting some value into the variable

	// Scalar Data Types
	// Integer
	integers()

	// Float
	float()

	// This will throw error due to Static Typing property of Golang
	// {
	// 	var x = 0
	// 	x = 4.3
	// 	x = "Shashank"
	// }

	// String
	strings()
	// rune()
	// bytes()

	// Pointer
	pointers()

	// Arrays
	arrays()

	// Slices
	slices()

	// Maps
	maps()

	// Custom data types
	custom()
}

func integers() {
	// In case bit size of integer variable is not specified, it is decided based on the bit size of the processor:
	// int32 on 32-bit systems, int64 on 64-bit systems
	var x int     // Declaring and defining a variable, golang self initializes the variable with default 0 value for the type
	var y int = 0 // Declaring, defining and initializing a variable manually
	z := 0        // Using shorthand to declare and initialize a variable, golang self defines the variable based on value

	x = 5
	y = 10
	z = 3000000000
	fmt.Println("value of x: ", x)
	fmt.Println("value of y: ", y)
	fmt.Println("value of z: ", z)

	// Size of integer data types
	var a int8  // Integer values from -128 to 127
	var b int16 // -32768 to 32767

	fmt.Println("value of a: ", a)
	fmt.Println("value of b: ", b)

	var c uint8  // Integer values from 0-255
	var d uint16 // 0 to 65535

	fmt.Println("value of c: ", c)
	fmt.Println("value of d: ", d)

	// TODO: int(4.3) cannot do this: untyped float constant
	// TODO: int(float(4.3)) cannot do this: float has no return type
	w := 4.3
	var e int = int(w)             // This will convert 4.3 to 4
	fmt.Println("value of e: ", e) // This will print 4
}

func float() {
	// This will throw errors: undefined
	// All variables need to be defined: what is the variable name, and the type of the values that the variable can contain
	// x = 5
	// y = 10
	// z = 3000000000
	// fmt.Println("value of x: ", x)
	// fmt.Println("value of y: ", y)
	// fmt.Println("value of z: ", z)

	// Float variables need to be defined with the bit size, i.e they cannot be float, but either float32 or float64
	var x, y, z float32 // Golang allows defining multiple variables of the same type in a single statement

	x = 5.74
	y = 10.68
	z = 3000000000.00000000
	fmt.Println("value of x: ", x)
	fmt.Println("value of y: ", y)
	fmt.Println("value of z: ", z)
}

func strings() {
	// Strings in Go are an immutable array of runes !!Important
	// A rune is a collectin of bytes ranging from 1 to 4
	// Strings in Golang are immutable
	// "Shashank": After saving this value in memory, this value cannot be modified
	// This value can be read, copied and a new value created out of it
	// String in Go are stored as their ASCII representations: this is a special type in Go called rune
	// "Shashank" will be storead as an array of runes on memory, each rune representing the ASCII value of a character
	// "A" = 65, "B" = 66 ..... this ASCII representation of a character is called a rune
	// TODO: Since strings are array of runes, they can be ranged over and each character of the string can be read

	var str string = "Shashank"
	str[0] = "x"
	fmt.Println(str)
}

func pointers() {
	// Stack: Data structure which follows LIFO(Last In First Out), consider example of a stack of plates
	// e.g let us have 5 plates, a, b, c, d and e
	// If I want to place these on top of each other, this will be the order:
	// plate e // this plate will come out at first(LIFO)
	// plate d
	// plate c
	// plate b
	// plate a

	// Heap: Data structure which is based on a tree data structure, i.e each entry points to another entry
	// Unordered
	// Ordering can be enforced by using min-heap(stores the smallest item at the root node), max-heap(opposite of min-heap)

	// Each program has two kinds of memory at runtime: stack, heap
	// Stack is faster, but memory size is limited
	// Heap is slower, but memory size is larger: Values on the heap can be accessed only through their memory address, if address is lost, value is lost even though it might exist on the heap

	// Pointers are special types in Go
	// Any variable of type pointer does not point to a value

	// e.g var x int = 0 // here x points to the value 0
	// var x *int // x points to a memory address, that memory location can only store an integer

	// Pointers have two signs associated with them:
	// *: Used to define the type of a variable as a pointer, or it is used to get the actual value from a pointer variable
	// &: Used to get the memory address of a value stored stored in a variable

	// Variable of pointer type points to a address of a memory location
	var x *int // This means that x will contain address of a memory location that can only contain integer values

	// TODO: x = &5 cannot do this: address of untyped constant
	y := 5
	x = &y // & is used to get the memory location of a variable

	// z := "Shashank"
	// x = &z cannot do this: x is a pointer of type integer, which means the location it points, can only have integer values

	fmt.Println("value of y: ", y) // Prints 5
	fmt.Println("value of x: ", x) // Prints address where 5 is stored

	fmt.Println("dereferenced value of x: ", *x) // dereferencing // This prints 5, as * is used to declare pointer types and to get value contained at a memory location
}

func arrays() {
	// List with all the list items being of the same data type, either scalar or vector
	// Arrays are of immutable sizes: size of an array cannot change at runtime, and must be known at compile time
	// In Go, size of the array is also part of the data type
	// Occupies contiguous memory location: in an array of 10 items, all items will be stored on the memory one after the other

	var arr1 [10]string
	// var arr2 [20]string

	// arr1 != arr2
	// arr1 = arr2 // Invalid code: size of the array is also part of the data type

	// Arrays are 0-indexed
	// In an array of type [10]string: [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" ]
	// To access individual items: arr1[0], arr1[1], arr1[2], arr1[3]...
	// Position of items in arrays starts from 0

	arr1[0] = "Shashank" // Adds this string to 1st position, or 0th index in arr1
	// arr1[0-1] = "Shashank" // Invalid Code: Indexing starts from 0 only, negative indices are invalid

	// arr1[10] = "Priyadarshi" // Invalid code: Indexing starts from 0, so index of 10th item will be = 10 - 1 = 9
	arr1[10-1] = "Priyadarshi"

	// {
	// 	var arr [10]string
	// 	var arr [11]string
	// }

	// arr1[10+1] = "Priyadarshi" // Invalid Code: This array is of size 10 items, and arrays are of immutable sizes
	// Index 10+1 means trying to access 11th items from a list of 10 items

	arr1 = [10]string{"Shashank", "Priyadarshi", "Golang", "Rust", "JavaScript", "TypeScript", "C", "C++", "Python", "R"}

	// TODO 1:
	// Declare two arrays of type int and type string
	// Fill integer array with strings
	// Fill string array with integers

	// TODO 2:
	// Create another array
	// This array should also contain integers
	// Try adding negative values into this array
	// All values in this array will be limited to 0-255
}

func slices() {
	// Size of an array is part of its type: var arr [10]string: here 10 is the size of the array
	// Since Go is statically typed, type of variable arr is fixes as [10]string, which means it will always store a maximum 10 strings
	// Type of variable arr will not change at runtime

	// Slices offer a solution for dynamically sized lists
	// Sizes of these lists grow based on requirement at runtime
	// Slices use arrays internally to store data
	// A slice is golang has three properties: length, capacity, type

	// var s []string // We declare a slice and define its type by not providing the size
	// If size provided, it becomes an array, and size is fixed for the array

	s2 := make([]string, 0, 10) // Declaration is done by shorthand :=, definition & initialization is done by the make function
	// Slice: The size specifies the length. The capacity of the slice is
	// equal to its length. A second integer argument may be provided to
	// specify a different capacity; it must be no smaller than the
	// length. For example, make([]int, 0, 10) allocates an underlying array
	// of size 10 and returns a slice of length 0 and capacity 10 that is
	// backed by this underlying array.

	// Length of a slice is the number of items the slice currently holds
	// Capacity is the number of items the slice can hold
	// The capacity of a slice can change based on requirement
	s2[11] = "Shashank" // The same case would be invalid for an array because an array of size 10 will have highest index of 10 -1 = 9

	// Internally, a slice stores data in an array
	// If type of slice is specified, an array of same type is created, using the capacity of the slice
	// If number of items goes more than the capacity, a new array of larger capacity is created, all items are moved from old array to new array

	// TODO 3:
	// Declare a slice of type string
	// Define the length and capacity at declaration
	// Do not initialize the slice
	// Then, put an item in the list at index greater than the capacity

}

func maps() {
	// Lists: Allow access to data in constant time: because location of the data is known
	// []int{0,1,2,3,4,5,6,7,8,9}: This is a list/array/slice of 10 items
	// To access the item at 6th position(5th index), I only need to do list[5]
	// The problem is: there can be multiple occurences of same item in a list
	// []string{"Shashank Priyadarshi", "Shashank P", "P Shashank", "Shashank Priyadarshi"}
	// []int{0,0,0,0,0,0}
	// Exactly once occurence cannot be ensured just by using lists
	// A map in Go solves this problem by storing unique items
	// A map is a list of Key Value pairs
	// map[int]string{1: "Shashank Priyadarshi", 2: "Shashank P", 3: "P Shashank", 4: "Shashank Priyadarshi"}
	// map[string]int{"Shashank Priyadarshi": 100000, "Shashank P": 5, "P Shashank": 500, "Shashank Priyadarshi": 5000}

	var x map[int]string
	y := map[int]string{}
	z := make(map[int]string)

	m = map[string]int{"Shashank Priyadarshi": 100000, "Shashank P": 5, "P Shashank": 500, "Shashank Priya": 5000}

	for i := 0; i < 3; i++ {
		fmt.Println(i)
		for key, value := range m {
			fmt.Print(key, " ", value, " ")
		}
		fmt.Println()
	}

	fmt.Println(x, y, z)

	// In the following list []int{0,1,2,3,4,5,6,7,8,9}: operation list[5] will always return the 6th item that is 5
	// In the following map map[int]string{1: "Shashank Priyadarshi", 2: "Shashank P", 3: "P Shashank", 4: "Shashank Priyadarshi"},
	// although m[1] will always return "Shashank Priyadarshi"
	// On printing the whole map, the order of key value pairs will change
	// In Go, maps are not ordered

	list := []int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	fmt.Println(list)
	fmt.Println(list)

	for k, v := range list {
		fmt.Print(k, ":", v, " , ")
	}

	fmt.Println()

	for k, v := range list {
		fmt.Print(k, ":", v, " , ")
	}

	fmt.Println()
	xMap := map[int]string{1: "Shashank Priyadarshi", 2: "Shashank P", 3: "P Shashank", 4: "Shashank Priyadarshi"}
	fmt.Println(xMap)
	fmt.Println(xMap)

	for k, v := range xMap {
		fmt.Print(k, ":", v, " , ")
	}

	fmt.Println()

	for k, v := range xMap {
		fmt.Print(k, ":", v, " , ")
	}

	fmt.Println()

	for k, v := range xMap {
		fmt.Print(k, ":", v, " , ")
	}

	// Maps in Go store key and values
	// Keys are always unique in a map
	// Values for two keys can be same in a Go map
	// If two different values for same key are received for a map, the map will overwrite older value with newer value
	xMap = map[int]string{1: "Shashank Priyadarshi", 2: "Shashank P", 3: "P Shashank", 4: "Shashank Priyadarshi"}
	fmt.Println(xMap)

	xMap[1] = "Naveen Patturi"
	fmt.Println(xMap)

	// TODO: 4
	// Create a map of with key of type integer and value of type string
	// Try to put these keys into the map with random values: "some_str0", "some_str1"

	// TODO: 5
	// Create a map with key of type interface{} and value of type string: definition of this map will be map[interface{}]string
	// Then, try to perform the same operation on the map as above
}

func custom() {
	type Fruits string
	const (
		// enums in Go
		Mango  Fruits = "mango"
		Banana Fruits = "banana"
		Apple  Fruits = "apple"
	)

	type Weekday string
	var (
		Sunday  Weekday
		Monday  Weekday
		Tuesday Weekday
	)

	type DayOfMonth int
	var (
		First  DayOfMonth
		Second DayOfMonth
	)
}

func structs() {
	// Object Oriented Programming: Classes and Objects
	// Define classes, each class has some properties and methods
	// Objects are instances of these classes
{
	type InteligenceLevel int8
	const (
		Poor InteligenceLevel = iota
		Average
		Good
		Excellent
	)

	type Animal struct {
		// These are properties of the class Animal
		Name             string
		Species          string
		InteligenceLevel InteligenceLevel // Poor, Average, Good, Excellent starting from 0
		Age              int
		Weight           int
	}

	// Dog is a class which inherits from Animal
	// However unline in other languages like Java, where there are keywords like implements, extends to enable Inheritance
	// In Go there are no specific keywords to enable Inheritance
	type Dog struct {
		Animal Animal // Composition instead of Inheritance
		Breed  string
	}

	type Cat struct {
		Animal Animal
		Breed  string
	}

	// Speak is a method of the class Animal
	// This is a generic speak method applicable for all animals
	// It accepts speech string as argument
	// This argument represents how different animals speak
	func (a Animal) Speak(animal, speech string) {
		fmt.Println(fmt.Sprintf("%s is %s", animal, speech))
	}

	func (d Dog) Speak() { // Receiver functions or methods as they are called in Go
		d.Animal.Speak("dog", "barking")
	}

	func (c Cat) Speak() {
		c.Animal.Speak("cat", "meowing")
	}

	dog := Dog {
		Animal: Animal{
			Name:             "Tommy",
			Species:          "Dog",
			InteligenceLevel: Good,
			Age:              5,
			Weight:           20,
		},
		Breed: "Labrador",
	}

	dog.Speak()

	// TODO: Create an employee class
	// Create an Address class
	// Employee will have name, age, level(enum), addresses
	// Create UpdateAddress method for an employee whenever a new address is passed
	// Create an employee object and invoke the UpdateAddress method
}
}

type Level int8

const (
	Fresher Level = iota
	Associate
	Senior
	Lead
	Manager
	Architect
	VP
	CEO
)

type Employee struct {
	// A struct can have any number of properties
	// Type of these properties can be any scalar, vector, custom or composite data type
	// Properties of a struct are called fields
	// Fields of a struct can be accessed using the dot operator

	// For this employee class, if we create an instance: object
	// For that object, the age, level, salary and address are subject to change
	// This is called behaviour of the employee class
	// Behaviour of a class is defined by methods
	Name    string
	Age     string
	Level   Level
	Salary  string
	Address Address
}

func (e Employee) NotifyBirthday() {
	// Start a timer at every birthday for next year's birthday
	// Whenever the timer stops, send a "Happy Birthday" notification to the employee
	// Start the timer again for next year
}

func (e Employee) UpdateAddress(street, city, state, pincode string) {
	e.Address = Address{
		Street:  street,
		City:    city,
		State:   state,
		Pincode: pincode,
	}
}

type Address struct {
	Street  string
	City    string
	State   string
	Pincode string
}

// Object Oriented Design

// Objects are instances of classes: variables of a particular class type
// Class can be any identity, its properties and behaviours

// Inheritance
// Encapsulation
// Abstraction
// Polymorphism

/*
Control structures
Functions
Parameters
Return values
Multiple return values
*/

func ControlStructures() {

	x := "Shashank"

	// If you have written some logic
	// Based on some condition, certain logic should be executed, some logic should be skipped

	if x == "Shashank" {
		fmt.Println(x)
	}

	switch x {
	case "Shashank":
		fmt.Println(x)
	default:
		fmt.Println("unknown person")
	}
}

// x, y, z, a, b, c are all function inputs
// when func Functions is called, these values should be provided in the same order
// ... is a special operator, allowing variadic parameterization
// Variadic Parameters: When number/type of input to function is unknown, use variadic interface{}
// Functions(1,2, "a", "b", true, false, 1, 2,3,4,5,6)
func Functions(x, y int, z, a string, b, c bool, args ...interface{}) (bool, error) {
	return true, nil
}

// Code is executed sequential
// package main

// func init(){}
// func main(){
// apiCall := httpclient.Do("https://example.com") // started
// add := 2 + 3 // started
// }

// API Call: response might take 1 second
// Concurrency vs Parallelism:
// Concurrency: Multiple executions happening asynchronously but not simultaneously
// Parallelism: Multiple executions happening asynchronously, mandatorily simultaneously

// Operating System uses Kernel to manages threads and processes using SysCalls
// Processes: Any running program is a process, network alloc, mem alloc, resource alloc, e.g. P1, P2 will have separate resources
// Threads: Part of a process is a thread, shares the resources of parent process, e.g. T1, T2 will share resoures of parent process P1

// Golang runtime manages the threads and processes
// All the developer has to do is use the go keyword

func Concurrency() {

	// Channels are datatypes in Go
	// make() function is used to create channels
	// Buffered channel, unbuffered channel
	// Unbuffered channels are synchronous channels: both sender and receiver should be present
	// Buffered channels are channels with data storage capacity: sender needs to be present, receiver can receive at its convenience, asynchronous
	done := make(chan bool)

	for i := 0; i < 10; i++ {

		// goroutine
		// Abstraction over OS threads and processes, and is managed by the Go runtime
		go func(i int) {
			req := &http.Request{
				Method: "GET",
				URL: &url.URL{
					Host: "https://example.com/" + string(i),
				},
				Host: "https://example.com",
			}

			client := http.Client{}

			client.Do(req)

			<-done
		}(i)

		// Run a for loop
		// Print numbers from 1 to 10 in that for loop
		// Print numbers from 1 to 10 in go routine
		// Channels are used to send data to and from goroutines
		for i := 0; i < 10; i++ {
			fmt.Println(i) // sync
		}

		for i := 0; i < 10; i++ {
			// async achieved using go routine, is concurrency, which means fmt.Println(i) is getting executed for different of i at the same time
			go fmt.Println(i)
		}

		time.Sleep(5 * time.Second)
	}

	done <- true
}

// closure
func Closure() {
	f := dummy()
	f()
}

func dummy() func() {
	x := 5

	return func() {
		fmt.Println(x)
	}
	// variable x should not be accessible after dummy() has executed, but it does
}

// Go Workspaces
// $GOPATH: bin/, pkg/, src/
// Go workspaces allow multiple modules inside the same workspace
// Primarily meant for development

// Concurrency
// Understanding the Go model of concurrency
// Goroutines
// Channels and coordination

// Closures
// Maps
// Errors and error handling
// Workspaces
// Pointers to Structs
// Arrays and Maps of Structs
// Implicitness of Interfaces
