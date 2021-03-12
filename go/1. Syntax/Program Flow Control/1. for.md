# 반복문
- 초기화 및 조건식이 있는 반복문
```go
package main 

import "fmt"

func main() {
	sum := 0
	// for 문에 초기화 구문, 조건식, 후속 작업 정의
	for i :=0; i < 10; i++ {
		sum += i
    }
    fmt.Println(sum)
}
```

- 조건식 사용하는 반복문 (while문과 비슷함)
```go
package main

import "fmt"

func main() {
	sum, i :=0, 0
	// for 문에 조건식만 사용
	for i < 10 {
		sum += i 
		i++
    }
    fmt.Println(sum)
}
```

 - for 문에 조건식이 없는 경우 (무한 루프)
```go
package main
 
import "fmt"

func main() {
	sum, i := 0, 0
	for {
		if i >= 10 {
			break
		}
		sum += i
		i++
	}
}
```