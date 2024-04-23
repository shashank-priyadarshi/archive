package types

import "fmt"

// Statically Typed Languages: Types are static after they have been defined for a variable
// Dynamically Typed Languages: Types are dynamic, which means types of variables can change within the same scope based no value
// Following code will work in JavaScript(dynamically typed), but not in Golang(statically typed):
// var x = 0
// x = 4.3
// x = "Shashank"

// Scalar data types: Numbers and Strings
// Vector data types: Arrays, Slices and Maps
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

	// Pointer
	pointers()
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
	// Strings in Golang are immutable
	// "Shashank": After saving this value in memory, this value cannot be modified
	// This value can be read, copied and a new value created out of it
	// String in Go are stored as their ASCII representations: this is a special type in Go called rune
	// "Shashank" will be storead as an array of runes on memory, each rune representing the ASCII value of a character
	// "A" = 65, "B" = 66 ..... this ASCII representation of a character is called a rune
	// TODO: Since strings are array of runes, they can be ranged over and each character of the string can be read

	var str string = "Shashank"
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
