package main

import (
    "fmt"
)

func diagonalDifference(arr [][]int32) int32 {
    // Write your code here
    /*              0,4
                1,3
            2,2
        3,1
    4,0*/
    N := len(arr)
    var sum1 int32 = 0
    
    fmt.Println("MATRIX:", arr, "N", N)
    
    for i:=0; i<N; i++ {
        for j:=0; j<N; j++ {
            if i==j {
                sum1 += arr[i][j]
                fmt.Println("ROW A(", i, ",", j, ")", arr[i][j])  
            }
        }
    }

    var sum2 int32 = 0

    for i:=0; i<N; i++ {
        for j:=0; j<N; j++ {
            if (j+i) == (N-1) {
                sum2 += arr[i][j]
                fmt.Println("ROW B(", i, ",", j, ")", arr[i][j])  
            }
        }
    }

    return Abs(sum1 - sum2)
}

func Abs(x int32) int32 {
    if x < 0 {
        return -x
    }
    return x
}

func main() {
    var matrix = [][]int32{
        {11,2,4},
        {4,5,6},
        {10,8,-12},
    }
    /*
    var matrix = [][]int32{
        {1,2,3},
        {4,5,6},
        {7,8,9},
    }
    */
    /*
    var matrix = [][]int32{
        {-1,0,1},
        {2,-1,5},
        {1,0,-1},
    }*/

    var r = diagonalDifference(matrix)
    fmt.Println(r)
}