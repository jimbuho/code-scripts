package main

import (
    "fmt"
    "strings"
    "strconv"
)

func staircase(n int32) {
    // Write your code here
    /*
       #
      ##
     ###
    ####
    */

    for i:=1; i<=int(n); i++ {
        str := "%"+strconv.Itoa(int(n))+"v\n"
        fmt.Printf(str, strings.Repeat("#", i))
    }
}

func main() {
    staircase(6)
}