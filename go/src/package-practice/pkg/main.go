package main

import (
	"fmt"
	"package-practice/lib"
)

func main() {
	fmt.Println(lib.IsDigit('1'))  // lib 패키지의 isDigit 사용
	fmt.Println(lib.IsDigit('a'))  // lib 패키지의 isDigit 사용
	fmt.Println(lib.isSpace('\t')) // 접근 제한
}
