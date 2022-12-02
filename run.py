from factory import create_app
app = create_app()
app.run(host="172.25.73.10",port="8080",debug=True)