# Getting Started

## [Overview of Go Programming Language](https://www.geeksforgeeks.org/golang/)

Go is a [statically typed](https://medium.com/nerd-for-tech/statically-typed-vs-strongly-typed-7537b2766c80), [systems programming language](https://medium.com/@arnoldnashwel/system-programming-language-f3bc1061984b).

```js
// Dynamic Typing
var x = 10; // integer
console.log(10);

x = "messing up data types"; // string
console.log(x);
```

```go
// Static Typing
var x = 10; // integer
fmt.Println(x);

x = "messing up data types"; // string, incompatible assignment
```

## Setting up Go Development Environment

- [Installing Go](https://go.dev/doc/install)
- Do `go version` to verify go installation.
- [Go environment variables](https://medium.com/@souravchoudhary0306/go-your-own-way-customizing-go-with-environment-variables-3e47c880fe34):
  - `GOROOT`: Path to go binary and standard library, usually something like `/usr/local/go` on Linux
  - [`GOPATH`](https://go.dev/wiki/SettingGOPATH): Developer workspace that contains go application source code, dependencies & go application binaries
  - `GOBIN`: Default path to Go application binaries, usually `$GOPATH/bin`

- Modules: Top level parent collection of packages constituting application code
- Packages: Collection of functions providing one functionality, e.g. strings package allows working with strings
  - Package name required as the first line of a go file
  - `package main` and `func main` are required for any go program to run
  - Package name should be unique
  - There cannot be more than one package in a single directory, except package names suffixed with `_test`

## [Working with Packages and Modules](https://go.dev/ref/mod#modules-overview)

## Basics of Go Syntax and Conventions

- Package
- Functions and the main() function
- Importing and using packages
- Variables
- Struct
- Members
- Anonymous members
- Interfaces
- Defining interfaces
- Implicitness of Interfaces
- panic and recover
- defer
- Concurrency
