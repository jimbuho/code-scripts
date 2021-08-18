package main

import (
    "fmt"
    "sort"
)


func birthdayCakeCandles(candles []int32) int32 {
    // Write your code here

    N := len(candles)
    candlesIntList := make([]int, N)

    for i, val := range candles {
      candlesIntList[i] = int(val)
    }

    sort.Ints(candlesIntList)
    
    //fmt.Println(candlesIntList)

    max := candlesIntList[N-1]
    counter := 1
    for i:=N-2; i>=0; i-- {
        //fmt.Println("[",i,"] = ",candlesIntList[i], ", Max", max, "Counter", counter)
        if candlesIntList[i] == max {
            counter += 1
        } else {
            break
        }
    }
    return int32(counter)
}

func main() {
    var candles = []int32 {1,2}
    var r = birthdayCakeCandles(candles)
    fmt.Println("Tallest:", r)
}