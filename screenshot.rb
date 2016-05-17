#!/usr/bin/env ruby

# ABOUT:      creates a number of screenshots for all video files in a directory
# ATTENTION:  make sure to  run `gem install streamio-ffmpeg`
# USAGE:      converter.rb <source dir> <target dir>

require "rubygems"
require "streamio-ffmpeg"

# CONFIGURATION:
NUMBER_OF_SCREENSHOTS = 3
RESOLUTION = "200x120"
OUTPUT_FORMAT = ".jpg"
VALID_EXTENSIONS = [".mp4", "m4v"]
PRESERVE_ASPECT_RATIO = :width  # or :height

class Converter
  def initialize
    @source, @target = validate_args()
    Dir.foreach(@source) do |file|
      if VALID_EXTENSIONS.include? File.extname(file)
        take_screenshots(file)
        puts "took screenshots for #{file}"
      else
        puts "#{file} has an invalid format"
      end
    end
    puts "done!"
  end

  def validate_args
    if ARGV.length != 2
      puts "usage: converter.rb <source dir> <target dir>"
      exit
    end
    return check_dir(ARGV[0]), check_dir(ARGV[1])
  end

  def check_dir(dir)
    if not File.directory? dir
      puts "unfortunately #{dir} is no directory :("
      exit
    end
    return dir
  end

  def take_screenshots(filename)
    source_path = File.join(@source, filename)
    movie = FFMPEG::Movie.new(source_path)
    NUMBER_OF_SCREENSHOTS.times do |i|
      take_screenshot(i + 1, filename, movie)
    end
  end

  def take_screenshot(counter, source_name, movie)
    seek_time = (movie.duration / (NUMBER_OF_SCREENSHOTS + 1) * (counter)).round
    settings = { seek_time: seek_time, resolution: RESOLUTION }
    target_name = File.basename(source_name, ".*") + "_" + counter.to_s + OUTPUT_FORMAT
    target_path = File.join(@target, target_name)
    movie.screenshot(target_path, settings, preserve_aspect_ratio: PRESERVE_ASPECT_RATIO)
  end
end

Converter.new