-- upgrade --
CREATE TABLE IF NOT EXISTS "clientSettings" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INT NOT NULL UNIQUE,
    "prefixes" JSON NOT NULL,
    "statistics" JSON NOT NULL,
    "quote_setting" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "defaultClient" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INT NOT NULL UNIQUE,
    "permission" INT NOT NULL  DEFAULT 0,
    "access_token" VARCHAR(198) NOT NULL,
    "created_user" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "nickname" VARCHAR(60) NOT NULL  DEFAULT 'MultiLilite best.',
    "out_time_connection" TIMESTAMP,
    "update_connection" TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
