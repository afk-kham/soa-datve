package main

import (
	"encoding/json"
	"net/http"
)

func writeJSON(w http.ResponseWriter, code int, value any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(code)
	_ = json.NewEncoder(w).Encode(value)
}
func success(w http.ResponseWriter, data any) {
	writeJSON(w, 200, struct {
		Status string `json:"status"`
		Data   any    `json:"data"`
	}{"success", data})
}
func failure(w http.ResponseWriter, code int, message string) {
	writeJSON(w, code, struct {
		Status  string `json:"status"`
		Message string `json:"message"`
	}{"error", message})
}
