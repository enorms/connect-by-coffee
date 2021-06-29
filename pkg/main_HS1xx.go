package main

import (
	"fmt"

	"github.com/sausheong/hs1xxplug"
)

func main() {
	plug := hs1xxplug.Hs1xxPlug{IPAddress: "192.168.87.255"}
	results, err := plug.MeterInfo()
	if err != nil {
		fmt.Println("err:", err)
	}
	fmt.Println(results)

}

/** SAMPLE for KP115 plug

** SUCCESS **
pkg % go run main_HS1xx.go
Cannot connnect to plug: dial tcp 192.168.87.255:9999: connect: permission denied
err: dial tcp 192.168.87.255:9999: connect: permission denied


** FAIL **
pkg % go run main_HS1xx.go
Cannot connnect to plug: dial tcp 192.168.88.255:9999: i/o timeout
err: dial tcp 192.168.88.255:9999: i/o timeout

*/
