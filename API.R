library(dplyr)        
library(httr)         
library(stringr)      
library(tidyr)        

base <- read.csv("C:/Users/.csv", fileEncoding = "Latin1",header = T,stringsAsFactors = F)

api_Key <- "Your API key"

generate_streetview_link <- function(lat, lon, key) {
  base_url <- "https://maps.googleapis.com/maps/api/streetview"
  query_params <- list(
    location = paste(lat, lon, sep = ","),
    size = "640x480",
    key = key
  )
  url <- modify_url(base_url, query = query_params)
  return(url)
}

base$STREETVIEW_IMG <- mapply(generate_streetview_link, base$latitud, base$longitud, api_Key)

generate_streetview_url <- function(lat, lon) {
  base_url <- "https://www.google.com/maps/@"
  coords <- paste(lat, lon, sep = ",")
  url <- paste(base_url, coords, ",3a,75y,114.26h,90t/data=!3m4!1e1!3m2!1s", coords, "!2e0", sep = "")
  return(url)
}
base$STREETVIEW_LINK <- mapply(generate_streetview_url, base$latitud, base$longitud)