package subtract

func Subtract(a, b int) int {
	if a < b {
		return b - a
	}
	return a - b
}
