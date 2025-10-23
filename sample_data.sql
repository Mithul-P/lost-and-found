USE lost_and_found;

INSERT INTO users (name, email, phone) VALUES ('Alice','alice@example.com','9999999999'), ('Bob','bob@example.com','8888888888');

INSERT INTO items (title,description,category,status,location,event_date,image_path,reporter_id) VALUES
('Black backpack','Black Nike backpack with red zipper','bags','lost','Library','2025-10-10',NULL,1),
('Set of keys','Bunch of keys with a blue tag','accessories','found','Cafeteria','2025-10-12',NULL,2),
('Earphones','Wireless earphones in case','electronics','lost','Auditorium','2025-10-08',NULL,1);
