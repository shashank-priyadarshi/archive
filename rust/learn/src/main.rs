// Entry point is fn main of main.rs
// Variable/Function names should be snake case not kebab case
fn main() {
    println!("Hello, world!");

    types();
    mutability();
    human("Shashank", 25, 5.11);
}

// Hoisting is allowed so functions can be declared before or after invocation
fn types() {
    {
        primitive_data_type() // Last line does not require semi colon and automatically returns
    }
    {
        arrays();
        tuples();
        slices()
    }
}

// Primitive Data Types
// int, float, bool, char

// Integer
// i8, i16, i32, i64, i128: Signed
// u8, u16, u32, u64, u128: Unsigned

// Float
// f32, f64

// Boolean
// true, false

// Char
// Single Unicode scalar value

fn primitive_data_type() {
    let integer: i8 = 42;
    println!("Value of integer 8: {}", integer);

    let float: f32 = 3.14;
    println!("Value of float 32: {}", float);

    let boolean: bool = true;
    println!("Value of boolean: {}", boolean);

    let character: char = 'z';
    println!("Value of character: {}", character);
}

// Compound Data Types
// array, tuple, slice, string(string slice)

// Arrays
// Fixed size contiguous collection of homogeneous data
fn arrays() {
    let numbers: [i8; 5] = [1, 2, 3, 4, 5]; // Type contains the data type of array elements, and the actual size of the array
    // Rust has two types of formats: Debuggable({:?}) and Display({})
    // Since [i8: 5] does not implement Display, it is not possible to print it using Display format({})
    println!("Values in the array of integer 8: {:?}", numbers);

    // Rust has strings and string slices
    // &str is a reference to a string, and is a string slice stored on the stack
    // String is a growable, mutable, owned string type which is allocated on the heap
    let fruits: [&str; 3] = ["Apple", "Banana", "Pineapple"];
    println!("Values in the array of string slices: {:?}", fruits);
}

// Tuples
// Heterogeneous collection of data of varying types
fn tuples() {
    let human: (String, i8, bool) = ("Shashank".to_string(), 25, true);
    println!("Values in tuple: {:?}", human);
}

// Slices
// View into a dynamic size contiguous collection of homogenous data
fn slices() {
    let numbers: &[i8] = &[1, 2];
    println!("Values in number slice: {:?}", numbers);

    let strings: &[&String] = &[&"Elephant".to_string(), &"Lion".to_string()];
    println!("Values in strings slice: {:?}", strings);
}

// All variables in Rust are immutable by default
// mut
fn mutability() {
    let mut state: String = String::from("");
    println!("I am {}", state);

    state.clear();
    state.push_str("not good, meh!");
    println!("Now, I am {}", state);

    let slice: &str = &state[..4];
    println!("Value of string slice is {}", slice);

    // state = "new_value".to_string(); Invalid code as borrowed variables cannot be reassigned
    // println!("New value of string slice is {}", slice)
}

// Functions
fn human(name: &str, age: u8, height: f32) {
    println!("Human details are:\n Name: {}\n Age: {}\n Height: {}\n", name, age, height);
}

// Expressions and Statements
// Expressions return a value
// Statements do not return a value
fn expressions() -> i32 {
    let total = {
        let price = 5;
        let qty = 10;
        price * qty
    };

    return total;
}
