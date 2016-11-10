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

var dollarMatch = regexp.MustCompile(`\$[0-9.,]+`)

func main() {
	start := "https://gist.githubusercontent.com/jorinvo/6f68380dd07e5db3cf5fd48b2465bb04/raw/c02b1e0b45ecb2e54b36e4410d0631a66d474323/fd0d929f-966f-4d1a-89cd-feee5a1c5347.json"
	var total float64
	visited := map[string]bool{}
	urls := []string{start}

	for len(urls) > 0 {
		url := urls[0]
		urls = urls[1:]
		t := struct {
			ID      string
			Content string
			Links   []string
		}{}
		err := getJSON(url, &t)
		if err != nil {
			log.Printf("failed to get JSON from '%s': %v", url, err)
		}

		if t.ID == "" || visited[t.ID] {
			continue
		}
		visited[t.ID] = true

		s := dollarMatch.FindString(t.Content)
		s = strings.Trim(s, "$,.")
		s = strings.Replace(s, ",", ".", 1)
		dollar, err := strconv.ParseFloat(s, 64)
		if err != nil {
			log.Fatal(err)
		}
		total += dollar
		urls = append(urls, t.Links...)
	}

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
