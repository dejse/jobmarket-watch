# Job Scrapper
library(httr2)
library(tidyverse)
library(rvest)
library(lubridate)
library(fs)
library(glue)

# Get today's date
today <- today() |> as.character()

# List of links to scrape
link_list <- c(
  "https://www.karriere.at/jobs/controller/wien",
  "https://www.karriere.at/jobs/controller/linz",
  "https://www.karriere.at/jobs/controller/salzburg",
  "https://www.karriere.at/jobs/controller/graz",
  "https://www.karriere.at/jobs/controller/innsbruck",
  "https://www.karriere.at/jobs/controller/vorarlberg"
)

# Read existing data or create new data frame
if (fs::file_exists("./data/data.csv")) {
  df <- read_csv("./data/data.csv", col_types = cols(
    date = col_character(),
    title = col_character(),
    location = col_character(),
    job_count = col_integer()
  ))
} else {
  df <- tibble(
    date = character(),
    title = character(),
    location = character(),
    job_count = integer()
  )
}

# Process each link
for (link in link_list) {
  response <- NULL
  max_retries <- 3
  
  # Retry logic
  for (attempt in 1:max_retries) {
    tryCatch({
      response <- request(link) |>
        req_timeout(5) |>
        req_headers(
          "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ) |>
        req_perform()
      
      if (resp_status(response) == 200) {
        break
      } else {
        print(glue("Attempt {attempt}: Status code {resp_status(response)} from {link}"))
      }
    }, error = function(e) {
      print(glue("Attempt {attempt}: Request failed for {link} - {conditionprint(e)}"))
    })
  }
  
  # Check if request was successful
  if (is.null(response) || resp_status(response) != 200) {
    print(glue("Failed to retrieve data from {link} after {max_retries} attempts"))
    next
  }
  
  # Parse HTML and extract job count
  html_content <- resp_body_html(response)
  title_element <- html_content |>
    html_element(".m-jobsListHeader__title")
  
  if (!is.na(title_element)) {
    title <- html_text(title_element) |> str_trim()
    
    # Extract job count using regex
    match <- str_extract(title, "\\d+")
    job_count <- ifelse(!is.na(match), as.integer(match), 0L)
    
    # Extract location from URL
    location <- str_split(link, "/")[[1]] |>
      tail(1) |>
      str_to_title()
    
    # Create new row
    new_row <- tibble(
      date = today,
      title = title,
      location = location,
      job_count = job_count
    )
    
    # Append to dataframe
    df <- df |> bind_rows(new_row)
  } else {
    print(glue("Could not find title element for {link}"))
  }
}

# Display dataframe
df

# Save to CSV
write_csv(df, "./data/data.csv")
