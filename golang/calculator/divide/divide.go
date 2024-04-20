package divide

import "fmt"

func Divide(a, b int) int {
	if b == 0 {
		fmt.Println("Dividing by 0 not allowed") // Error return & error handling
		return 0
	}
	return a / b
}
