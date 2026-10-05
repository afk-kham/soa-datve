package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
)

type Config struct{ HTTPAddr, DBHost, DBPort, DBName, DBUser, DBPassword string }

func env(key, fallback string) string {
	if v, ok := os.LookupEnv(key); ok {
		return v
	}
	return fallback
}
func loadConfig() (Config, error) {
	c := Config{env("HTTP_ADDR", "0.0.0.0:5006"), env("DB_HOST", "127.0.0.1"), env("DB_PORT", "3306"), env("DB_NAME", "notification_db"), env("DB_USER", ""), env("DB_PASSWORD", "")}
	_, port, err := net.SplitHostPort(c.HTTPAddr)
	if err != nil {
		return c, fmt.Errorf("HTTP_ADDR phải có dạng host:port")
	}
	for _, p := range []string{port, c.DBPort} {
		n, e := strconv.Atoi(p)
		if e != nil || n < 1 || n > 65535 {
			return c, fmt.Errorf("cổng phải trong khoảng 1–65535")
		}
	}
	if strings.TrimSpace(c.DBHost) == "" || strings.TrimSpace(c.DBName) == "" || strings.TrimSpace(c.DBUser) == "" {
		return c, fmt.Errorf("DB_HOST, DB_NAME và DB_USER không được rỗng")
	}
	return c, nil
}
