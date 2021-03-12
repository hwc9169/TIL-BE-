# Switch Case 문
- case 문에 조건식이 사용된다.
- 조건식이 참이라면 밑의 명령어를 실행한다.
```go
package main

import "fmt"

func main() {
	c := 'a'
	
	switch {
	// case문에 조건식 사용
	case '0' <= c && c <= '9':
		fmt.Printf("%c(은)는 숫자입니다.", c)
	case 'a' <= c && c <= 'z':
		fmt.Printf("%c(은)는 소문자입니다.", c)
	case 'A' <= c && c <= 'Z':
		fmt.Printf("%c(은)는 대문자입니다.", c)
    }
}
```