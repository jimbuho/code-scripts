package main

import (
    "fmt"
    "sort"
)

type byValue []int32

func (f byValue) Len() int {
    return len(f)
}

func (f byValue) Less(i, j int) bool {
    return f[i] < f[j]
}

func (f byValue) Swap(i, j int) {
    f[i], f[j] = f[j], f[i]
}


/*
 * Complete the 'miniMaxSum' function below.
 *
 * The function accepts INTEGER_ARRAY arr as parameter.
 */

func miniMaxSum(arr []int32) {
    // Write your code here
    sort.Sort(byValue(arr))

    fmt.Println(arr)

    var min int64 = 0
    for i:=0; i<4; i++ {
        min += int64(arr[i])
    }

    sort.Sort(sort.Reverse(byValue(arr)))

    fmt.Println(arr)

    var max int64 = 0
    for i:=0; i<4; i++ {
        max += int64(arr[i])
    }

    fmt.Printf("%d %d\n", min, max)
}

func main() {
    var arr = []int32 {123232, 33432423, 54324234, 74233, 9343};

    miniMaxSum(arr)
}