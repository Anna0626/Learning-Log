# view 

> 날짜: 2026-01-29
> 원본 노션: [링크](https://www.notion.so/view-2f7b28703eb0800a87a8f8946f128ffa)

---

# VIEW

가상의 테이블

```sql
SELECT * FROM boardview;
```

- 실제 데이터를 저장 ❌
- SELECT 결과를 이름 붙여 저장한 것
- 테이블처럼 SELECT 가능
### VIEW의 목적

- 복잡한 쿼리 단순화
- 보안
- 재사용성
---

### VIEW 생성

```sql
CREATE VIEW 뷰이름 AS
SELECT 컬럼들
FROM 테이블
WHERE 조건;
```

```sql
CREATE VIEW boardview AS
SELECT b.board_no, b.title, m.user_id
FROM board b
JOIN member m ON b.writer = m.user_id;

```

---

### CREATE OR REPLACE VIEW

```sql
CREATE OR REPLACE VIEW 뷰이름 AS
SELECT ...
```

- 뷰가 없으면 → 생성
- 뷰가 있으면 → 덮어쓰기(수정)
- 기존 VIEW 삭제할 필요 없음
---

### ALTER VIEW

```sql
ALTER VIEW 뷰이름 AS
SELECT ...
```

- 기존 VIEW 정의 변경
- MySQL / MariaDB에서 사용 가능
- 실무에서는 보통
- CREATE OR REPLACE VIEW 를 더 많이 씀
---

### VIEW 구조 확인

```sql
SHOW CREATE VIEW boardview;
```

- VIEW를 만들 때 사용된 원본 SQL 확인 가능
---

### VIEW 삭제

```sql
DROP VIEW 뷰이름;
```

예시

```sql
SELECT * FROM boardview WHERE user_id = 'lee';
```

```sql
CREATE TABLE member(
   user_no INT(11) NOT NULL AUTO_INCREMENT,
   user_id VARCHAR(20) NOT NULL,
   user_pw VARCHAR(20) NOT NULL,
   user_name VARCHAR(15) NOT NULL,
   user_email VARCHAR(30) NOT NULL,
   user_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
   user_del INT(1) NOT NULL DEFAULT '5',
   PRIMARY KEY (user_no),
   UNIQUE user_id(user_id)
);

CREATE TABLE board(
   board_no INT(11) NOT NULL AUTO_INCREMENT,
   board_title VARCHAR(50) NOT NULL,
   board_content VARCHAR(5000) NOT NULL,
   user_no INT(11) NOT NULL,
   board_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
   board_like INT(11) NULL DEFAULT '0',
   board_del INT(1) NOT NULL DEFAULT '1',
   PRIMARY KEY (board_no),
   CONSTRAINT fk___user2 FOREIGN KEY (user_no) REFERENCES member(user_no)
);

INSERT INTO board(board_title, board_content, user_no)
VALUES ('두번째 글', '본문내용', 1);

SELECT * FROM board 
UPDATE board SET board_del = 0 WHERE board_no=9;

SELECT b.board_no, b.board_title, b.board_date, b.board_like, m.user_name
FROM board b JOIN member m ON b.user_no=m.user_no
WHERE b.board_del=1
ORDER BY b.board_no DESC;
```

