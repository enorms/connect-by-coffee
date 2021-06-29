package main

import (
	"log"
	"time"

	"github.com/jaedle/golang-tplink-hs100/pkg/configuration"
	"github.com/jaedle/golang-tplink-hs100/pkg/hs100"
)

func main() {
    // check WiFi address in settings
    devices, err := hs100.Discover("192.168.87.0/24",
        configuration.Default().WithTimeout(time.Second),
    )
    if err != nil {
        panic(err)
    }
    log.Printf("Found devices: %d", len(devices))
    for _, d := range devices {
        name, _ := d.GetName()
        log.Printf("Device name: %s", name)
    }
}

/** SAMPLE
eric@mbp-16 synesti % go run main.go
2021/06/28 22:38:21 Found devices: 1
2021/06/28 22:38:21 Device name: plug_tm
*/