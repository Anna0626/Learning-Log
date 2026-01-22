# SubQuery, IUD

> 날짜: 2026-01-22
> 원본 노션: [링크](https://www.notion.so/SubQuery-IUD-2f0b28703eb0805889b1c94e03246624)

---

# SubQuery(서브 쿼리)

하나의 SQL 문 안에 포함되어 실행 결과를 제공하는 또 다른 SELECT 문

```java
SELECT 컬럼
FROM 테이블
WHERE 컬럼 연산자 (SELECT 컬럼
                   FROM 테이블
                   WHERE 조건);

```

### 예시

salaries 테이블에서 salary의 평균보다 salary를 많이 받는 상위 10명 출력 

```java
SELECT *
FROM salaries
WHERE salary >= (	SELECT AVG(salary)
						FROM salaries
						WHERE to_date = '9999-01-01' ) 
						AND to_date = '9999-01-01'
ORDER BY salary DESC 
LIMIT 10;

```

---

# INSERT

```sql
INSERT INTO 테이블명 (컬럼명) VALUES (컬럼에 들어갈 값);
```

### 예시

testboard  테이블에 행('책 제목', '작가님', '내용') 추가 

```sql
INSERT INTO testboard (title, writer, content)
		VALUES ('책 제목', '작가님', '내용');
```

### 다중 입력

```sql
INSERT INTO 테이블명 (컬럼명) 
VALUES (컬럼에 들어갈 값),
			 (컬럼에 들어갈 값),
			        •
			        •
			 (컬럼에 들어갈 값);
```

### key 값 

한 번 삭제되었던 key의 값은 다시 사용하지 X

---

# UPDATE

```sql
UPDATE 테이블명 SET 컬럼명 = 값, 컬럼명 = 값, 컬럼명 = 값 WHERE NO = 값;
```

### 예시

testboard 테이블에서 key의 값이 7인 행의 title을 ‘수정’으로 업데이트

```sql
UPDATE testboard SET title = '수정' WHERE NO = 7;
```

testboard 테이블에서 key의 값이 7인 행의 date를 현재 시간으로 업데이트

```sql
UPDATE testboard SET DATE =NOW() WHERE NO =7; 
```

---

# DELETE

```sql
DELETE FROM 테이블명 WHERE KEY = 값 
```

### 예시 

testboard 테이블에서 writer이 3PO인 행 삭제

```sql
DELETE FROM testboard WHERE writer = '3PO';
```



