#!/usr/bin/env ruby

puts "=== Script starting ==="
STDOUT.flush

begin
  require 'net/http'
  require 'uri'
  require 'fileutils'
  require 'open-uri'
  require 'optparse'
rescue => e
  puts "ERROR LOADING LIBRARIES: #{e.message}"
  puts e.backtrace
  exit 1
end

def log(message)
  puts message
  STDOUT.flush
end

# Browser-like request headers
def browser_headers
  {
    'User-Agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept' => 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language' => 'en-US,en;q=0.5',
    'Connection' => 'keep-alive',
    'Upgrade-Insecure-Requests' => '1',
    'Pragma' => 'no-cache',
    'Cache-Control' => 'no-cache'
  }
end

# Enhanced HTTP request function with browser headers
def fetch_with_headers(uri_str)
  uri = URI(uri_str)
  request = Net::HTTP::Get.new(uri)
  
  # Add browser-like headers
  browser_headers.each do |key, value|
    request[key] = value
  end
  
  # Set up the HTTP connection with SSL support if needed
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = (uri.scheme == 'https')
  http.verify_mode = OpenSSL::SSL::VERIFY_NONE
  http.open_timeout = 30
  http.read_timeout = 30
  
  log "  Making request to: #{uri_str}"
  response = http.request(request)
  
  return response
end

log "=== Web Scraper Tool ==="

# Parse command line options
options = {}
option_parser = OptionParser.new do |opts|
  opts.banner = "Usage: web-scraping.rb [options]"
  
  opts.on("--url URL", "URL to scrape") do |url|
    options[:url] = url
  end
  
  opts.on("-h", "--help", "Show this help message") do
    puts opts
    exit
  end
end

begin
  option_parser.parse!
rescue OptionParser::InvalidOption => e
  log "ERROR: #{e.message}"
  puts option_parser
  exit 1
end

# Get URL either from command line options or user input
url = options[:url]

if url.nil?
  log "Enter URL to scrape (include http:// or https://): "
  STDOUT.flush
  url = gets
  if url.nil?
    log "ERROR: Could not read from standard input!"
    exit 1
  end
  url = url.chomp
end

log "Using URL: #{url}"

begin
  # Validate URL
  uri = URI.parse(url)
  unless uri.scheme && uri.host
    log "Error: Invalid URL format. Please include http:// or https://"
    exit 1
  end

  # Create directory structure
  domain = uri.host.gsub(/^www\./, '')
  output_dir = File.join(File.dirname(File.dirname(__FILE__)), "user", "scraped websites", domain)
  FileUtils.mkdir_p(output_dir)

  log "Scraping #{url}..."

  # Use the enhanced request function for main page
  response = fetch_with_headers(url)

  if response.code == "200"
    # Save main page
    File.open(File.join(output_dir, "index.html"), "w") do |file|
      file.write(response.body)
    end
    log "Main page saved to #{output_dir}/index.html"
    
    # Extract and save linked resources (CSS, JS, images)
    log "Looking for linked resources..."
    resources = response.body.scan(/(href|src)=["']([^"']+)["']/).map { |match| match[1] }
    log "Found #{resources.length} potential resources to download"
    
    # Initialize counters
    successful_downloads = 0
    skipped_resources = 0
    failed_downloads = 0
    
    resources.each_with_index do |resource_url, index|
      if resource_url.start_with?('#', 'mailto:', 'tel:') || resource_url.empty?
        skipped_resources += 1
        next
      end
      
      begin
        # Convert relative URLs to absolute
        resource_uri = if resource_url.start_with?('http://', 'https://')
                        URI.parse(resource_url)
                      else
                        resource_path = resource_url.start_with?('/') ? resource_url : "/#{resource_url}"
                        URI.parse("#{uri.scheme}://#{uri.host}#{resource_path}")
                      end
        
        # Create subdirectory for resource if needed
        resource_path = resource_uri.path
        resource_filename = File.basename(resource_path)
        # Handle empty filenames
        resource_filename = "index.html" if resource_filename.empty? || resource_filename == "/"
        resource_dir = File.join(output_dir, File.dirname(resource_path).gsub(/^\//, ''))
        
        log "[#{index+1}/#{resources.length}] Downloading: #{resource_url}"
        
        FileUtils.mkdir_p(resource_dir) unless File.directory?(resource_dir)
        
        # Download resource with browser-like headers
        begin
          # Use the enhanced request method
          res_response = fetch_with_headers(resource_uri.to_s)
          
          if res_response.code == "200"
            File.open(File.join(resource_dir, resource_filename), "wb") do |file|
              file.write(res_response.body)
            end
            log "  ✓ Saved to: #{resource_dir}/#{resource_filename}"
            successful_downloads += 1
          elsif res_response.code == "301" || res_response.code == "302"
            redirect_location = res_response['location']
            log "  ↳ Following redirect: #{resource_uri} -> #{redirect_location}"
            
            redirect_response = fetch_with_headers(redirect_location)
            if redirect_response.code == "200"
              File.open(File.join(resource_dir, resource_filename), "wb") do |file|
                file.write(redirect_response.body)
              end
              log "  ✓ Saved to: #{resource_dir}/#{resource_filename} (after redirect)"
              successful_downloads += 1
            else
              log "  ✗ Failed after redirect: HTTP #{redirect_response.code}"
              failed_downloads += 1
            end
          else
            log "  ✗ Failed to download: HTTP #{res_response.code}"
            failed_downloads += 1
          end
        rescue => e
          log "  ✗ Could not download resource: #{resource_url}"
          log "    Error: #{e.message}"
          failed_downloads += 1
        end
      rescue => e
        log "  ✗ Failed to process resource URL: #{resource_url}"
        log "    Error: #{e.message}"
        failed_downloads += 1
      end
    end
    
    # Print summary
    log "\nScraping completed!"
    log "------------------------------"
    log "Total resources found: #{resources.length}"
    log "Successfully downloaded: #{successful_downloads}"
    log "Skipped: #{skipped_resources}"
    log "Failed: #{failed_downloads}"
    log "Website scraped and saved to: #{output_dir}"
    
    # Add a clear completion marker
    log "=== SCRAPING FINISHED SUCCESSFULLY ==="
    
    # Exit with successful status code
    exit 0
  else
    log "Error: Could not access the website. HTTP response code: #{response.code}"
    exit 1
  end
rescue => e
  log "Error occurred while scraping: #{e.message}"
  exit 1
end