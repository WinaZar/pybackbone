data "external_schema" "sqlalchemy" {
    program = [
        "poetry",
        "run",
        "python",
        "-m",
        "src",
        "generate-migrations"
    ]
}

env "sqlalchemy" {
  src = data.external_schema.sqlalchemy.url
  dev = "docker://postgres/16/dev"
  migration {
    dir = "file://migrations"
  }
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}
