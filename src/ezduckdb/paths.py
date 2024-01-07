from pathlib import Path


class S3AwarePath(type(Path())):
    def is_s3(self):
        return self.parts[0] == "s3:"

    def __str__(self):
        if self.is_s3():
            return f"s3://{super().__str__()[4:]}"
        else:
            return super().__str__()

    def get_s3_bucket(self):
        if self.is_s3():
            return self.parts[1]
        else:
            raise Exception("Not an S3 path")

    def get_s3_prefix(self):
        if self.is_s3():
            return "/".join(self.parts[2:])
        else:
            raise Exception("Not an S3 path")

    def get_table_name(self):
        if self.stem.count("_") < 1:
            raise Exception(
                "Not a valid format. Needs at least 1 `_` to match format `<schema_name>_<table_name>`"
            )
        schema_name = self.stem.split("_")[0]
        table_name = self.stem[len(schema_name) + 1 :]
        return schema_name, table_name
