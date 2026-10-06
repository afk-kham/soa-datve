package userservice;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Helper dung chung cho HTTP response cua User/Auth Service.
 *
 * Chuc nang:
 * - Tra JSON response
 * - CORS cho Client/Admin
 * - Tra 204 No Content
 * - Tra 200/201/... voi data
 * - Tra loi JSON voi message
 */
public final class Http {

    private Http() {
        // Khong cho tao object
    }

    private static final Gson GSON = new GsonBuilder()
            .serializeNulls()
            .create();

    /**
     * Cau hinh CORS chung.
     *
     * Hien tai cho phep Client/Admin chay localhost:
     * - http://localhost:8080
     * - http://127.0.0.1:8080
     * - http://localhost:8081
     * - http://127.0.0.1:8081
     *
     * Neu sau nay deploy domain that thi sua lai danh sach nay.
     */
    private static void setCorsHeaders(HttpExchange ex) {
        String origin = ex.getRequestHeaders().getFirst("Origin");

        if (origin != null &&
                (origin.equals("http://localhost:8080")
                        || origin.equals("http://127.0.0.1:8080")
                        || origin.equals("http://localhost:8081")
                        || origin.equals("http://127.0.0.1:8081"))) {

            ex.getResponseHeaders().set("Access-Control-Allow-Origin", origin);
            ex.getResponseHeaders().set("Vary", "Origin");
        }

        ex.getResponseHeaders().set(
                "Access-Control-Allow-Methods",
                "GET, POST, PUT, DELETE, OPTIONS"
        );

        ex.getResponseHeaders().set(
                "Access-Control-Allow-Headers",
                "Content-Type, Authorization"
        );

        ex.getResponseHeaders().set(
                "Access-Control-Max-Age",
                "3600"
        );
    }

    /**
     * Tra HTTP 204 No Content.
     *
     * Duoc Main.java su dung cho OPTIONS/preflight.
     */
    public static void noContent(HttpExchange ex) throws IOException {
        setCorsHeaders(ex);

        ex.sendResponseHeaders(204, -1);
    }

    /**
     * Tra response thanh JSON.
     *
     * Vi du:
     * Http.success(ex, 200, data);
     * Http.success(ex, 201, data);
     */
    public static void success(
            HttpExchange ex,
            int status,
            Object data
    ) throws IOException {

        setCorsHeaders(ex);

        ex.getResponseHeaders().set(
                "Content-Type",
                "application/json; charset=UTF-8"
        );

        String json = GSON.toJson(data);
        byte[] body = json.getBytes(StandardCharsets.UTF_8);

        ex.sendResponseHeaders(status, body.length);

        try {
            ex.getResponseBody().write(body);
        } finally {
            ex.getResponseBody().close();
        }
    }

    /**
     * Tra response loi JSON.
     *
     * Dang response hien tai:
     * {
     *   "error": "Noi dung loi"
     * }
     *
     * Dang nay phu hop voi Main.java hien tai.
     */
    public static void error(
            HttpExchange ex,
            int status,
            String message
    ) throws IOException {

        setCorsHeaders(ex);

        ex.getResponseHeaders().set(
                "Content-Type",
                "application/json; charset=UTF-8"
        );

        Map<String, String> bodyData = new LinkedHashMap<>();
        bodyData.put("error", message);

        String json = GSON.toJson(bodyData);
        byte[] body = json.getBytes(StandardCharsets.UTF_8);

        ex.sendResponseHeaders(status, body.length);

        try {
            ex.getResponseBody().write(body);
        } finally {
            ex.getResponseBody().close();
        }
    }
}