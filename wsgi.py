from app import app, IO

if __name__ == "__main__":
    app.config["IO"] = IO()
    app.run()