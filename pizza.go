package main

import "fmt"

func main() {
	p := NewPizza()
	p.WithBase(Standard).
		WithToppings([]Toppings{PineApple}).
		Cook()

	fmt.Println(p.Price())
}

type Base int

const (
	Standard Base = iota
)

func (b Base) Price() float32 {
	switch b {
	case Standard:
		return 1
	default:
		return 0
	}
}

type Toppings int

const (
	PineApple Toppings = iota
)

func (t Toppings) Price() float32 {
	switch t {
	case PineApple:
		return .20
	default:
		return 0
	}
}

type Pizza struct {
	base     Base
	toppings []Toppings
	price    float32
}

// constructor
func NewPizza() Pizza {
	return Pizza{}
}

func (p Pizza) WithBase(b Base) Pizza {
	p.base = b
	return p
}
func (p Pizza) WithToppings(t []Toppings) Pizza {
	p.toppings = t
	return p
}

func (p Pizza) Cook() {
	var total float32
	for _, topping := range p.toppings {
		total += topping.Price()
	}

	p.price = total + p.base.Price()
	return
}

func (p Pizza) Price() float32 {
	return p.price
}
