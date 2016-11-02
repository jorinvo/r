package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"regexp"
	"strconv"
	"strings"
)

func main() {
	start := "https://gist.githubusercontent.com/jorinvo/5459a9d1f1cf44c5d637866355266021/raw/0a9eb60b-c25b-4af8-aab9-4b56bb1e0489.json"
	dollarMatch := regexp.MustCompile(`(\$[0-9.,]+)|([0-9.,]+\$)`)
	var total float64
	done := make(map[string]bool)
	urls := make(chan string, 1000)
	urls <- start

	for {
		select {
		case url := <-urls:
			if done[url] {
				break
			}
			done[url] = true

			d := struct {
				Content string
				Links   []string
			}{}
			getJSON(url, &d)

			str := dollarMatch.FindString(d.Content)
			str = strings.Replace(str, "$", "", 1)
			str = strings.Replace(str, ",", ".", 1)
			dollar, err := strconv.ParseFloat(str, 64)
			fatal(err)
			total += dollar

			for _, link := range d.Links {
				urls <- link
			}
		default:
			fmt.Printf("Total: $%.2f", total)
			close(urls)
			return
		}
	}
}

func getJSON(url string, target interface{}) {
	r, err := http.Get(url)
	fatal(err)
	defer func() {
		err := r.Body.Close()
		fatal(err)
	}()
	err = json.NewDecoder(r.Body).Decode(&target)
	fatal(err)
}

func fatal(err error) {
	if err != nil {
		log.Fatal(err)
	}
}
