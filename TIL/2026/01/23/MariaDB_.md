# MariaDB 

> 날짜: 2026-01-23
> 원본 노션: [링크](https://www.notion.so/MariaDB-2f1b28703eb080e5920bd282e85f940c)

---

# ubuntu 환경에서 MariaDB 

### 환경 설정 

```sql
sudo apt update 
sudo apt upgrade 
sudo apt install mariadb-server
```

### 접속 

```sql
sudo mariadb -u root -p 
```

### 데이터베이스 확인 

### 데이터 베이스 생성 

```sql
create database 데이터베이스명;
```

### 작업할 데이터베이스 선택

```sql
USE 데이터베이스명;
```

### 테이블 생성 

```sql
CREATE TABLE 테이블명;
```

### 테이블 확인

```sql
show tables;
```

### DB가 이 쿼리를 어떻게 처리할지 설명

```sql
EXPLAIN 쿼리문;
```

## 권한

### 모든 권한 부여

```sql
GRANT ALL PRIVILEGES ON DB명.* 
TO 사용자명@'%' 
IDENTIFIED BY 'pwd설정';
```

- GRANT ALL PRIVILEGES : 
SELECT, INSERT, UPDATE, DELETE, CREATE, DROP 등 모든 권한
- ON '사용자계정명’.* : '사용자계정명’ 데이터베이스 안의 모든 테이블
- '%' : 어디서든 접속 가능
- IDENTIFIED BY 'pwd설정' : 비밀번호 설정
예시

```sql
GRANT ALL PRIVILEGES ON dswu04.* 
TO lee@'%' 
IDENTIFIED BY 'ck319gh';
```

lee라는 사용자에게 dswu04 데이터베이스의 모든 권한을 부여

비밀번호를 ck319gh로 설정

### 사용자 계정을 생성 후 권한 부여

```sql
CREATE USER '사용자계정명'@'%' IDENTIFIED 'pwd설정';
GRANT ALL PRIVILEGES ON DB명.* TO '사용자계정명'@'%';
```

- CREATE USER '사용자계정명’ : 사용자 계정을 생성
- IDENTIFIED : 비밀번호 설정 
- '%' : 어디서든 접속 가능
### 모든 사용자 계정 목록 조회

```sql
SELECT host, user FROM mysql.user;
```


| host | user |
| --- | --- |
| % | lee |
| localhost | root |

### 권한 회수 

```sql
REVOKE ALL ON DB명.* FROM '사용자계정명'@'접근범위';
```

- REVOKE : 권한을 회수(박탈) 하는 명령어
- ALL : 객체(DB명.*)에 대해 부여된 권한만 회수함
- ON DB명.* : 데이터베이스 그 안의 모든 테이블 (*)
- 접근범위 
예시

```sql
GRANT ALL ON test.* TO 'user1'@'%';
REVOKE ALL ON test.* FROM 'user1'@'%';
```

- user1은:
계정은 살아 있고, 권한만 사라짐

---

### jdk

개발 환경 구축 / 개발 / 컴파일 등 

- openjdk-17-jdk
- openjdk-17-jdkeadless
### jre

실행 환경 구축 / 실행만 가능   

- openjdk-17-jre
- openjdk-17-jre-headless
### headless 

- GUI(awt, swing)가 제거된 버전
- 가벼운 버전
- 텍스트 환경용
### openjdk-17-jre-zero

- 기본 jre는 cpu에 맞춰서 개발한 어셈블리코드가 들어간다
- 하지만 zero는 어셈블리코드가 없고(zero) 인터프리터 방식으로 구동된다. 
- 속도는 느리지만 어떤 cpu에서도 동작한다. 
- zero는 새로운 하드웨어 환경용

| 일반 jre | jre-zero |
| --- | --- |
| jit컴파일러 사용 | 인터프리터 방식 |
| 빠름 | 느림 |
| 특정 cpu에 맞게 제작
cpu구조에 의존 | 어떤 cpu에서도 동작함 |
| 일반 서버 구동시 사용 | 새로운 하드웨어 이식용 |

---

# putty 원격 접속 

1. putty 설치


1. ubuntu 서버에서 환경 구축  
1. ubuntu 서버 주소 확인 
1. putty 열어서 inet주소 넣기 
1. ubuntu 사용자명과 pwd를 넣으면 접속


