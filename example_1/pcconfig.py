import pynecone as pc

class ExampleConfig(pc.Config):
    pass

config = ExampleConfig(
    app_name="example_1",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)