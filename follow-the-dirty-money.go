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
	start := "https://gist.githubusercontent.com/jorinvo/5459a9d1f1cf44c5d637866355266021/raw/e8d9b8424b208f037a9075c5f18fdd05537b3cb2/0a9eb60b-c25b-4af8-aab9-4b56bb1e0489.json"
	dollarMatch := regexp.MustCompile(`(\$[0-9.,]+)|([0-9.,]+\$)`)
	var total float64
	done := make(map[string]bool)
	urls := make(chan string, 1000)
	urls <- start

	for {
		select {
		case url := <-urls:
			d := struct {
				ID      string
				Content string
				Links   []string
			}{}
			err := getJSON(url, &d)
			if err != nil {
				fmt.Printf("failed to fetch URL '%s': %v", url, err)
			}

			if done[d.ID] {
				break
			}
			done[d.ID] = true

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

func getJSON(url string, target interface{}) error {
	r, err := http.Get(url)
	if err != nil {
		return err
	}
	defer r.Body.Close()
	err = json.NewDecoder(r.Body).Decode(&target)
	return err
}

func fatal(err error) {
	if err != nil {
		log.Fatal(err)
	}
}
