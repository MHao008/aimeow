CREATE TABLE users (
   id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(50),
   age INT
);
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    amount DECIMAL(10,2)
);
// 插入测试数据
INSERT INTO users(name, age) VALUES('Alice',28),('Bob',35);
INSERT INTO orders(user_id, amount) VALUES(1,100.00),(2,150.00),(2,50.00);
