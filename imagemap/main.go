package main

import (
	"image"
	"image/color"
	"io/ioutil"
	"log"
	"math"
	"math/rand"
	"os"
	"path/filepath"
	"runtime"
	"sync"

	"github.com/disintegration/imaging"
)

type job struct {
	os.FileInfo
	pos int
}

type result struct {
	image.Image
	pos int
}

func main() {
	resultFile := "imagemap.jpg"
	tileSize := 300
	tilesPerRow := 10

	dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	fatal(err, "failed to get dir path")

	// log to file
	absLogFile := filepath.Join(dir, logfile)
	f, err := os.OpenFile(absLogFile, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	fatal(err, "failed to open log file")
	log.SetOutput(f)

	// get file list
	files, err := ioutil.ReadDir(imgDir)
	fatal(err, "failed to read tmp dir")
	if len(files) < 1 {
		log.Println("no images to process")
		os.Exit(0)
	}

	// shuffle file order
	// for algorithm see http://stackoverflow.com/a/12267471
	for i := range files {
		j := rand.Intn(i + 1)
		files[i], files[j] = files[j], files[i]
	}

	jobs := make(chan job)
	results := make(chan result)

	// read and resize images in parallel
	wg := waitForWorkers(len(files), func() {
		for j := range jobs {
			img, err := imaging.Open(filepath.Join(imgDir, j.Name()))
			fatal(err, "failed to open image")
			img = imaging.Fill(img, tileSize, tileSize, imaging.Center, imaging.Lanczos)
			results <- result{img, j.pos}
		}
	})

	// create result image
	width := tileSize * tilesPerRow
	height := int(math.Ceil(float64(len(files))/float64(tilesPerRow))) * tileSize
	resultImg := imaging.New(width, height, color.White)

	// insert results into result image
	go func() {
		for r := range results {
			pos := image.Point{
				X: (r.pos % tilesPerRow) * tileSize,
				Y: (r.pos / tilesPerRow) * tileSize,
			}
			resultImg = imaging.Paste(resultImg, r, pos)
		}
	}()

	// start workers with files
	for i, file := range files {
		jobs <- job{file, i}
	}

	// close channels and wait for workers
	close(jobs)
	wg.Wait()
	close(results)

	// save result
	err = imaging.Save(resultImg, resultFile)
	fatal(err, "unable to save image")
}

func waitForWorkers(maxWorkers int, worker func()) *sync.WaitGroup {
	numWorkers := runtime.NumCPU()
	if numWorkers > maxWorkers {
		numWorkers = maxWorkers
	}
	var wg sync.WaitGroup
	wg.Add(numWorkers)
	for w := 0; w < numWorkers; w++ {
		go func() {
			defer wg.Done()
			worker()
		}()
	}
	return &wg
}

func fatal(err error, msg string) {
	if err != nil {
		log.Println(msg)
		log.Println(err)
		os.Exit(1)
	}
}
