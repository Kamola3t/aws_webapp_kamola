Full Web Application Deployment on AWS (EC2, RDS, S3)

Here's a detailed explanation of the project:

PART 1: DATABASE SETUP WITH AMAZON RDS (PostgreSQL)

1)Download a Dataset from Kaggle: 
- go to https://www.kaggle.com/datasets
- Search for a dataset (e.g., sales data, movies, cars)
- Download the dataset in CSV format.

2)Launch RDS PostgreSQL Instance
- Log in to your AWS account.
- Go to RDS → Click Create Database.
- Choose Standard Create → Select PostgreSQL.
- Set your DB Instance Identifier (e.g., db_kamola).
- Set master username/password.
- Choose Free Tier.
- Launch the DB instance and wait for it to be available.

3)Create Database and Table
- Open DBeaver.
- Click New Connection → Choose PostgreSQL.
- Fill in:
Host: your-rds-endpoint;
Port: 5432; 
Database: postgres 
Username: your-username
Password: your-password
Click Test Connection → then Finish.

Run this SQL in DBeaver SQL Editor:
```sql
CREATE DATABASE db_<yourname>;
```

- Then run this to create a table:
```sql
CREATE TABLE tbl_<yourname>_disney_movies (
    movie_title TEXT,
    release_date DATE,
    genre TEXT,
    mpaa_rating TEXT,
    total_gross BIGINT,
    inflation_adjusted_gross BIGINT
);
```
It is an exaple, you need to change tbl_<yourname>_disney_movies with your name and dataset


PART 2: STATIC WEBSITE HOSTING ON AMAZON S3:

1) Create index HTML

Example:
```html
<!DOCTYPE html>
<html>
<head><title>My App</title></head>
<body>
  <h1>Welcome to My Web App</h1>
  <button onclick="addData()">Add Data</button>
  <button onclick="deleteData()">Delete Data</button>

  <script>
    function addData() {
      fetch('http://<your-ec2-public-ip>:5000/add', {method: 'POST'})
        .then(res => alert("Data added!"));
    }

    function deleteData() {
      fetch('http://<your-ec2-public-ip>:5000/delete', {method: 'POST'})
        .then(res => alert("Data deleted!"));
    }
  </script>
</body>
</html>
```

2) Create S3 Bucket
- Go to AWS Console > S3
- Click Create bucket
- Name: yourname-static-website
- Uncheck Block all public access
- Enable Static website hosting
- Upload index_yourname.html

3) Make Files Public:

Go to Permissions > Bucket Policy and paste:
```json
{
 "Version": "2012-10-17",
 "Statement": [
  {
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::yourname-static-website/*"
  }
 ]
}
```
arn:aws:s3:::yourname-static-website/ - replace it with your own.


PART 3: EC2 DEPLOYMENT

1) Launch EC2 Instance (Python Flask App)
- Choose Ubuntu Server 22.04
- Select t2.micro (Free tier)
- Open port 22 (SSH) and 5000 (Flask)
- Create & download .pem key

2) SSH and Setup
- Run: ssh -i yourkey.pem ubuntu@<your-ec2-public-ip>
replace with your key.pem and pulic ip

- To Install Python & dependencies run:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install flask psycopg2
```

- Create app.py
```python
from flask import Flask
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host='your-rds-endpoint',
    database='db_yourname',
    user='postgres',
    password='postgres'
)
cursor = conn.cursor()

@app.route('/add', methods=['POST'])
def add_data():
    cursor.execute("INSERT INTO tbl_yourname_sales_data (product_name, quantity_sold, sale_date) VALUES ('Product A', 10, CURRENT_DATE);")
    conn.commit()
    return "Added!"

@app.route('/delete', methods=['POST'])
def delete_data():
    cursor.execute("DELETE FROM tbl_yourname_sales_data WHERE product_name = 'Product A';")
    conn.commit()
    return "Deleted!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```


- Run Flask App:
```bash
python3 app.py
```

- now it is accessible :
```
http://<your-ec2-public-ip>:5000
```
put your public ip address in your instances.