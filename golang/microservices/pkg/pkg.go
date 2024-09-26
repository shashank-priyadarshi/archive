package pkg

import (
	"database/sql"
	"fmt"
)

func ExportedFunc() {
	d := Dog{"anything"}
	fmt.Println(d)

	a := Animal{
		Something: "Dog",
		name:      "Tommy",
	}

	a.Something = "Cat"
	a.name = "Tom"

	d2 := Dog{"Tommy"}
	fmt.Println(d2.string)

	conn, _ := sql.Open("mysql", "")
	_ = Service{DB: conn}

}

func unexportedFunc()

type Animal struct {
	int8      // anonymous property
	Something string
	name      string
}

func (Animal) Class1()
func (Animal) class1()

type animal struct{}

type Dog struct {
	string // anonymous property/member
}

type Service struct {
	*sql.DB // usecase for anonymous property/member
}
