-- Create "example_entity" table
CREATE TABLE "public"."example_entity" (
  "id" uuid NOT NULL,
  "name" character varying(255) NOT NULL,
  "description" character varying(1500) NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  "updated_at" timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY ("id")
);
