-- DROP TABLE IF EXISTS public."user";
CREATE TABLE public."user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
	active bool NULL DEFAULT TRUE
);


-- DROP TABLE IF EXISTS public."operation";
CREATE TABLE public."operation" (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) CHECK (type IN ('addition', 'subtraction', 'multiplication', 'division', 'square_root', 'random_string')) NOT NULL,
    cost int8 NOT NULL
);

INSERT INTO public."operation" ("type","cost") VALUES
	 ('addition',1),
	 ('subtraction',1),
	 ('multiplication',2),
	 ('division',3),
	 ('square_root',4),
	 ('random_string',10);


-- DROP TABLE IF EXISTS public."record";
CREATE TABLE public."record" (
    id SERIAL PRIMARY KEY,
    operation_id INT REFERENCES public."operation" (id) ON DELETE CASCADE,
    user_id INT REFERENCES public."user" (id) ON DELETE CASCADE,
    amount int8 NOT NULL,
    user_balance int8 NOT NULL,
    operation_response TEXT NOT NULL,
    deleted bool NULL DEFAULT FALSE,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
