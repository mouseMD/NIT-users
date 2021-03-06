def setup_config(app, env):
    config_data = {
        "DEBUG": env.bool("DEBUG", True),
        "HOST": env("HOST", "0.0.0.0"),
        "PORT": env.int("PORT", 8000),
        "DB_URL": env("DB_URL", "postgresql://postgres:postgres@localhost/postgres"),
        "OFFERS_URL": env("OFFERS_URL", "http://0.0.0.0:8001/offer")
    }
    app.update_config(config_data)
