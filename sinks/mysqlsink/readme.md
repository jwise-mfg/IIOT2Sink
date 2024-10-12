Requires `pip install mysql-connector` or `apt install python3-mysql.connector`

# Example database
```
CREATE DATABASE YOURDB;
CREATE USER 'YOURDBUSER'@'localhost' IDENTIFIED BY 'YOURDBPASSWORD';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER 
ON YOURDB.* TO 'YOURDBUSER'@'localhost' IDENTIFIED BY 'YOURDBPASSWORD';
FLUSH PRIVILEGES;
```
# Example table
```
CREATE TABLE `tag_samples` (
  `id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `label` varchar(255) NOT NULL,
  `value` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
ALTER TABLE `tag_samples` ADD PRIMARY KEY (`id`);
ALTER TABLE `tag_samples`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=252;
COMMIT;
```