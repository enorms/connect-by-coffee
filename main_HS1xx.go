package main

import (
	"fmt"

	"github.com/sausheong/hs1xxplug"
)

func another_main() {
	plug := hs1xxplug.Hs1xxPlug{IPAddress: "192.168.87.255"}
	results, err := plug.MeterInfo()
	if err != nil {
		fmt.Println("err:", err)
	}
	fmt.Println(results)

}

/** SAMPLE

eric@mbp-16 synesti % go run main.go
Cannot connnect to plug: dial tcp 192.168.87.255:9999: connect: permission denied
err: dial tcp 192.168.87.255:9999: connect: permission denied

*/
