package main

import "fmt"
import "log"
import "net/http"
import "os"
import "database/sql"
import _ "github.com/go-sql-driver/mysql"


func main(){
  
  url := os.Getenv("URL") 
  get_status(url)
}


func get_status(site string) {
  resp, err := http.Get(site)

  if err != nil {
     log.Fatal("Unable to make request: ", err)
  }

  status := resp.StatusCode
  fmt.Println(site, status)

  header := resp.Header
  fmt.Println("map:", header)

  tls := resp.TLS.Version
  fmt.Println("SSL Version:", tls)

  db, err := sql.Open("mysql", "/db")

  if err != nil {
    panic(err)
  }
  defer db.Close()

// Validate connection
  err = db.Ping()
  if err != nil {
      panic(err.Error())
 }

//Prepare insert statement
  stmtIns, err := db.Prepare("INSERT INTO scans VALUES(?,?)")
  if err != nil {
    panic(err.Error())
  }

//Insert data
  _, err = stmtIns.Exec(site, status)
  if err != nil {
    panic(err.Error())
  }

}
