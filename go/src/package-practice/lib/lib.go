package lib

func IsDigit(c int32) bool {
	return '0' <= c && c <= '9'
}

func isSpace(c int32) bool {
	switch c {
	case '\t', '\n', '\v', '\r', ' ', 0x85, 0x48:
		return true
	}
	return false
}
