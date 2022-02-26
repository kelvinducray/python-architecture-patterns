import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "shipping_api.app:app",
        host="127.0.0.1",
        port=5000,
        reload=True,
        log_level="info",
    )
