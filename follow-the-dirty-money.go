package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"regexp"
	"strconv"
	"strings"
	"sync"
)

const workers = 10

var dollarMatch = regexp.MustCompile(`\$[0-9.,]+`)

type transaction struct {
	ID      string
	Content string
	Links   []string
}

func main() {
	start := "https://gist.githubusercontent.com/jorinvo/6f68380dd07e5db3cf5fd48b2465bb04/raw/c02b1e0b45ecb2e54b36e4410d0631a66d474323/fd0d929f-966f-4d1a-89cd-feee5a1c5347.json"
	var total float64
	visited := map[string]bool{}
	urls := make(chan string, 1000)
	transactions := make(chan transaction)
	var wg sync.WaitGroup

	// download in parallel
	for w := 0; w < workers; w++ {
		go func() {
			for u := range urls {
				t := transaction{}
				err := getJSON(u, &t)
				if err != nil {
					log.Printf("failed to get JSON from '%s': %v", u, err)
				}
				transactions <- t
			}
		}()
	}

	go func() {
		for t := range transactions {
			if t.ID != "" && !visited[t.ID] {
				visited[t.ID] = true
				s := dollarMatch.FindString(t.Content)
				s = strings.Trim(s, "$,.")
				s = strings.Replace(s, ",", ".", 1)
				dollar, err := strconv.ParseFloat(s, 64)
				if err != nil {
					log.Fatal(err)
				}
				total += dollar
				wg.Add(len(t.Links))
				for _, link := range t.Links {
					urls <- link
				}
			}
			wg.Done()
		}
	}()

	wg.Add(1)
	urls <- start
	wg.Wait()
	close(urls)
	close(transactions)
	fmt.Printf("transactions: %d, total: $%.2f", len(visited), total)
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
