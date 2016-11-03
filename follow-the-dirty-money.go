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
	start := "https://gist.githubusercontent.com/jorinvo/eb3d2b39d1af49ccca8f2abcc3c56f6a/raw/d92a341af9bc82ab2a284f7f3a4e72f0cca20f5e/0fc12f66-ee24-4d9d-ab9e-6caeee1c93c7.json"
	dollarMatch := regexp.MustCompile(`\$[0-9.,]+`)
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
				log.Printf("failed to fetch URL '%s': %v", url, err)
				break
			}

			if done[d.ID] {
				break
			}
			done[d.ID] = true

			str := dollarMatch.FindString(d.Content)
			str = strings.Trim(str, "$,.")
			str = strings.Replace(str, ",", ".", 1)
			dollar, err := strconv.ParseFloat(str, 64)
			fatal(err)
			total += dollar

			for _, link := range d.Links {
				urls <- link
			}
		default:
			fmt.Printf("transactions: %d, total: $%.2f", len(done), total)
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
