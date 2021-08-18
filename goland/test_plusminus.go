package main

import (
    "fmt"
)

func plusMinus(arr []int32) {
    // Write your code here

    count_positive := 0
    count_negative := 0
    count_zero := 0
    
    N := len(arr)
    
    for i:=0;i<N; i++ {
        num := arr[i]
        
        if num < 0 {
            count_negative += 1
        } else if num > 0 {
            count_positive += 1
        } else  {
            count_zero += 1
        }
    }

    var posiveRatio float64 = float64(count_positive) / float64(N) 
    var negativeRatio float64 = float64(count_negative) / float64(N) 
    var zeroRatio float64 = float64(count_zero) / float64(N) 

    fmt.Printf("%.6f\n", posiveRatio)
    fmt.Printf("%.6f\n", negativeRatio)
    fmt.Printf("%.6f\n", zeroRatio)
}

func main() {
    var arr = []int32 {1,-1,0,1,-1}
    plusMinus(arr)
}